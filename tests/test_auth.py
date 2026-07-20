from unittest.mock import MagicMock, patch

import pytest

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
