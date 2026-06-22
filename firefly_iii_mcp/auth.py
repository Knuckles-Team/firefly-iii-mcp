#!/usr/bin/python

"""Authentication.

Priority:
1. **OIDC Delegation** (RFC 8693 Token Exchange) — when ``ENABLE_DELEGATION`` is
   active, exchanges the IdP-issued user token for a downstream access token via the
   shared ``agent_utilities.mcp.delegated_auth`` helper.
2. **Fixed credentials** — falls back to the ``FIREFLY_III_TOKEN`` env var.

For a multi-tenant service, add an ``instances.py`` that resolves a configured
instance NAME (from ``<service>_instances`` in ``~/.config/agent-utilities/config.json``)
to ``(url, token, verify)`` and call it here before the delegation/fixed paths — see
``gitlab_api.instances`` (CONCEPT:KG-2.9g) for the golden pattern.
"""

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

from .api import ApiClientFireflyIii

logger = get_logger(__name__)
_client = None


def get_client(
    url: str | None = None,
    token: str | None = None,
    verify: bool | None = None,
    config: dict | None = None,
) -> ApiClientFireflyIii:
    """Get or create a singleton API client (OIDC delegation or fixed credentials).

    Credentials resolve through the shared config layer (the one XDG
    ``config.json`` / env) at call time, not frozen at import.
    """
    global _client
    if _client is not None:
        return _client

    base_url = url or setting("FIREFLY_III_URL", "http://localhost:8080")
    token = token or setting("FIREFLY_III_TOKEN", "")
    if verify is None:
        verify = setting("FIREFLY_III_SSL_VERIFY", True)

    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        get_user_identity,
        is_delegation_enabled,
    )

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if is_delegation_enabled(config):
        try:
            delegated_token = get_delegated_token(
                config=config,
                audience=(config or {}).get("audience", base_url),
                scopes=(config or {}).get("delegated_scopes", "api"),
                verify=verify,
            )
            identity = get_user_identity()
            logger.info(
                "Using OIDC delegated token",
                extra={"user_email": identity.get("email"), "url": base_url},
            )
            _client = ApiClientFireflyIii(
                base_url=base_url, token=delegated_token, verify=verify
            )
            return _client
        except Exception as e:
            logger.error(
                "OIDC delegation failed",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            raise RuntimeError(f"Token exchange failed: {str(e)}") from e

    # --- Path 2: Fixed Credentials (FIREFLY_III_TOKEN) ---
    logger.info("Using fixed credentials")
    try:
        _client = ApiClientFireflyIii(base_url=base_url, token=token, verify=verify)
    except (AuthError, UnauthorizedError) as e:
        raise RuntimeError(
            f"AUTHENTICATION ERROR: The credentials provided are not valid for '{base_url}'. "
            f"Please check your FIREFLY_III_TOKEN and FIREFLY_III_URL environment variables. "
            f"Error details: {str(e)}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"AUTHENTICATION ERROR: Failed to instantiate client. "
            f"Error details: {str(e)}"
        ) from e

    return _client
