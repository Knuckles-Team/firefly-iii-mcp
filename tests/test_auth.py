from unittest.mock import MagicMock, patch

import pytest
from agent_connector_sdk.exceptions import AuthError

import firefly_iii_mcp.auth as auth_module
from firefly_iii_mcp.auth import get_client


@pytest.mark.concept("FF-OS.config.ff")
def test_get_client_auth_error():
    """Auth failure surfaces a clear error. CONCEPT:FF-OS.config.ff"""
    auth_module._client = None
    with patch("firefly_iii_mcp.auth.ApiClientFireflyIii") as mock_client_cls:
        mock_client_cls.side_effect = Exception("Auth Failure")
        with pytest.raises(RuntimeError) as exc_info:
            get_client(
                url="https://service.example.invalid",
                token="test-token",
                tls_profile=MagicMock(),
            )
        assert "AUTHENTICATION ERROR" in str(exc_info.value)
    auth_module._client = None


@pytest.mark.concept("FF-OS.config.ff")
def test_get_client_requires_url():
    """Neither an argument nor a configured URL raises a clear error."""
    auth_module._client = None
    with patch("firefly_iii_mcp.auth.setting", return_value=""):
        with pytest.raises(RuntimeError, match="FIREFLY_III_URL is required"):
            get_client(url=None, token="test-token", tls_profile=MagicMock())
    auth_module._client = None


@pytest.mark.concept("FF-OS.config.ff")
def test_get_client_requires_token_when_not_delegated():
    """Without delegation, a missing token raises a clear error."""
    auth_module._client = None
    with patch("firefly_iii_mcp.auth.setting", return_value=""):
        with pytest.raises(RuntimeError, match="FIREFLY_III_TOKEN is required"):
            get_client(
                url="https://service.example.invalid",
                token=None,
                tls_profile=MagicMock(),
            )
    auth_module._client = None


@pytest.mark.concept("FF-OS.config.ff")
def test_get_client_reuses_singleton_when_not_delegated():
    """A second call without delegation returns the cached client, not a new one."""
    auth_module._client = None
    with patch("firefly_iii_mcp.auth.ApiClientFireflyIii") as mock_client_cls:
        first = get_client(
            url="https://service.example.invalid",
            token="test-token",
            tls_profile=MagicMock(),
        )
        second = get_client(
            url="https://service.example.invalid",
            token="test-token",
            tls_profile=MagicMock(),
        )
        assert first is second
        mock_client_cls.assert_called_once()
    auth_module._client = None


@pytest.mark.concept("FF-OS.config.ff")
def test_get_client_rejects_configured_credentials():
    """A rejected fixed credential surfaces the specific auth-rejection message."""
    auth_module._client = None
    with patch("firefly_iii_mcp.auth.ApiClientFireflyIii") as mock_client_cls:
        mock_client_cls.side_effect = AuthError("nope")
        with pytest.raises(RuntimeError, match="credentials were rejected"):
            get_client(
                url="https://service.example.invalid",
                token="test-token",
                tls_profile=MagicMock(),
            )
    auth_module._client = None


@pytest.mark.concept("FF-OS.config.ff")
def test_get_client_delegated_uses_exchanged_token():
    """OIDC delegation exchanges the caller's token and always builds a fresh client."""
    auth_module._client = None
    profile = MagicMock()
    with (
        patch("firefly_iii_mcp.auth.ApiClientFireflyIii") as mock_client_cls,
        patch(
            "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
            return_value=True,
        ),
        patch(
            "agent_utilities.mcp.delegated_auth.get_delegated_token",
            return_value="exchanged-token",
        ),
    ):
        get_client(
            url="https://service.example.invalid",
            tls_profile=profile,
            config={"audience": "svc"},
        )
        mock_client_cls.assert_called_once_with(
            base_url="https://service.example.invalid",
            token="exchanged-token",
            tls_profile=profile,
        )
    auth_module._client = None


@pytest.mark.concept("FF-OS.config.ff")
def test_get_client_delegated_failure_cleans_up_profile():
    """A failed token exchange cleans up the TLS profile and raises a clear error."""
    auth_module._client = None
    profile = MagicMock()
    with (
        patch(
            "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
            return_value=True,
        ),
        patch(
            "agent_utilities.mcp.delegated_auth.get_delegated_token",
            side_effect=RuntimeError("exchange failed"),
        ),
    ):
        with pytest.raises(RuntimeError, match="Token exchange failed"):
            get_client(url="https://service.example.invalid", tls_profile=profile)
    profile.cleanup.assert_called_once()
    auth_module._client = None
