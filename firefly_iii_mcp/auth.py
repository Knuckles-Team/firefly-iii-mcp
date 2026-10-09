#!/usr/bin/python

"""Authentication.

Priority:
1. **OIDC Delegation** (RFC 8693 Token Exchange) — when ``ENABLE_DELEGATION`` is
   active, exchanges the IdP-issued user token for a downstream access token via the
   shared ``agent_utilities.mcp.delegated_auth`` helper.
2. **Fixed credentials** — falls back to the ``FIREFLY_III_TOKEN`` env var.

Endpoint and credential values are resolved at runtime through the shared
AgentConfig projection. TLS trust is a mandatory-verification profile resolved by
``agent_connector_sdk.tls.resolve``; this package never stores certificate
material or a machine-specific trust path.
"""

import logging
from typing import Any

from agent_connector_sdk.config import setting
from agent_connector_sdk.exceptions import AuthError, UnauthorizedError
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile

from .api import ApiClientFireflyIii

logger = logging.getLogger(__name__)
_client: ApiClientFireflyIii | None = None


def _resolve_firefly_credentials(
    url: str | None, token: str | None, delegated: bool
) -> tuple[str, str | None]:
    """Resolve the base URL and (non-delegated) token from args or config.

    Raises ``RuntimeError`` if a value required for the chosen auth mode is
    missing.
    """
    base_url = url or setting("FIREFLY_III_URL", "")
    if not base_url:
        raise RuntimeError("FIREFLY_III_URL is required")
    token = token or setting("FIREFLY_III_TOKEN", "")
    if not delegated and not token:
        raise RuntimeError("FIREFLY_III_TOKEN is required when delegation is disabled")
    return base_url, token


def _build_delegated_client(
    base_url: str,
    profile: ResolvedTLSProfile,
    config: dict[str, Any] | None,
) -> ApiClientFireflyIii:
    """Exchange the caller's IdP token for a downstream token (RFC 8693 Token
    Exchange) and build the client from it."""
    from agent_utilities.mcp.delegated_auth import get_delegated_token

    try:
        delegated_token = get_delegated_token(
            config=config,
            audience=(config or {}).get("audience", base_url),
            scopes=(config or {}).get("delegated_scopes", "api"),
        )
        logger.info("Using OIDC delegated credentials")
        return ApiClientFireflyIii(
            base_url=base_url,
            token=delegated_token,
            tls_profile=profile,
        )
    except Exception as e:
        profile.cleanup()
        logger.error(
            "OIDC delegation failed",
            extra={"error_type": type(e).__name__},
        )
        raise RuntimeError("Token exchange failed") from None


def _build_fixed_credential_client(
    base_url: str,
    token: str | None,
    profile: ResolvedTLSProfile,
) -> ApiClientFireflyIii:
    """Build the client from the fixed FIREFLY_III_TOKEN credential."""
    logger.info("Using fixed credentials")
    try:
        return ApiClientFireflyIii(
            base_url=base_url,
            token=token,
            tls_profile=profile,
        )
    except (AuthError, UnauthorizedError):
        profile.cleanup()
        raise RuntimeError(
            "AUTHENTICATION ERROR: The configured credentials were rejected. "
            "Check the runtime FIREFLY_III_TOKEN and FIREFLY_III_URL inputs."
        ) from None
    except Exception as e:
        profile.cleanup()
        raise RuntimeError(
            "AUTHENTICATION ERROR: Failed to instantiate the client "
            f"({type(e).__name__})."
        ) from None


def get_client(
    url: str | None = None,
    token: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
    config: dict[str, Any] | None = None,
) -> ApiClientFireflyIii:
    """Get or create a singleton API client (OIDC delegation or fixed credentials).

    Credentials resolve through the shared config layer (the one XDG
    ``config.json`` / env) at call time, not frozen at import.
    """
    global _client

    from agent_utilities.mcp.delegated_auth import is_delegation_enabled

    delegated = is_delegation_enabled(config)
    if not delegated and _client is not None:
        return _client

    base_url, token = _resolve_firefly_credentials(url, token, delegated)
    profile = tls_profile or resolve_tls_profile("firefly_iii")

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if delegated:
        return _build_delegated_client(base_url, profile, config)

    # --- Path 2: Fixed Credentials (FIREFLY_III_TOKEN) ---
    _client = _build_fixed_credential_client(base_url, token, profile)
    return _client
