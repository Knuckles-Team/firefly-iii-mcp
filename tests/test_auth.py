from unittest.mock import patch

import pytest

import firefly_iii_mcp.auth as auth_module
from firefly_iii_mcp.auth import get_client


@pytest.mark.concept("FF-001")
def test_get_client_auth_error():
    """Auth failure surfaces a clear error. CONCEPT:FF-001"""
    auth_module._client = None
    with patch("firefly_iii_mcp.auth.ApiClientFireflyIii") as mock_client_cls:
        mock_client_cls.side_effect = Exception("Auth Failure")
        with pytest.raises(RuntimeError) as exc_info:
            get_client()
        assert "AUTHENTICATION ERROR" in str(exc_info.value)
    auth_module._client = None
