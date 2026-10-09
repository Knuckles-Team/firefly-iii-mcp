#!/usr/bin/python

"""Authentication.

Priority:
1. **OIDC Delegation** (RFC 8693 Token Exchange) — when ``ENABLE_DELEGATION`` is
   active, exchanges the IdP-issued user token for a downstream access token via
   ``agent_connector_sdk.auth.delegation``.
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


def _is_delegation_enabled(config: dict[str, Any] | None) -> bool:
    """Whether the OIDC delegation path should be attempted.

    An explicit ``config`` dict (test injection only -- no production caller
    passes one) wins outright; otherwise reads the real ``ENABLE_DELEGATION``
    setting through ``agent_connector_sdk.auth.delegation.DelegationSettings``.
    """
    if config is not None:
        return bool(config.get("enable_delegation", False))
    from agent_connector_sdk.auth.delegation import DelegationSettings

    return DelegationSettings.from_settings().enabled


def _build_delegated_client(
    base_url: str,
    profile: ResolvedTLSProfile,
) -> ApiClientFireflyIii:
    """Exchange the caller's IdP token for a downstream token (RFC 8693 Token
    Exchange) and build the client from it.

    Reads delegation settings (``OIDC_TOKEN_URL``/``OIDC_CLIENT_ID``/
    ``OIDC_CLIENT_SECRET_REF``/``AUDIENCE``/``DELEGATED_SCOPES``) from the
    process settings via ``agent_connector_sdk.auth.delegation.DelegationSettings``;
    unlike the old ``agent_utilities`` helper, this has no per-call override for
    those fields, only for whether delegation is attempted at all (see
    :func:`_is_delegation_enabled`).
    """
    import httpx
    from agent_connector_sdk.auth.delegation import (
        DelegationSettings,
        current_user_token,
        exchange_token,
    )
    from agent_connector_sdk.exceptions import LoginRequiredError

    try:
        delegation_settings = DelegationSettings.from_settings()
        subject_token = current_user_token()
        if not subject_token:
            raise LoginRequiredError("no verified caller token to delegate")
        with httpx.Client(timeout=30) as http_client:
            access_token = exchange_token(
                delegation_settings,
                subject_token=subject_token,
                http_client=http_client,
            )
        logger.info("Using OIDC delegated credentials")
        return ApiClientFireflyIii(
            base_url=base_url,
            token=access_token.value,
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
    assert token is not None  # guaranteed by _resolve_firefly_credentials
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

    delegated = _is_delegation_enabled(config)
    if not delegated and _client is not None:
        return _client

    base_url, token = _resolve_firefly_credentials(url, token, delegated)
    profile = tls_profile or resolve_tls_profile("firefly_iii")

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if delegated:
        return _build_delegated_client(base_url, profile)

    # --- Path 2: Fixed Credentials (FIREFLY_III_TOKEN) ---
    _client = _build_fixed_credential_client(base_url, token, profile)
    return _client
