from unittest.mock import MagicMock, patch

import pytest

from firefly_iii_mcp.api import ApiClientBase


@pytest.mark.concept("FF-001")
def test_request_returns_json():
    """API client returns parsed JSON. CONCEPT:FF-001"""
    client = ApiClientBase(base_url="http://localhost", token="t")
    response = MagicMock()
    response.json.return_value = {"ok": True}
    with patch.object(client.session, "request", return_value=response):
        assert client.request("GET", "/health") == {"ok": True}
