from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_api_client():
    client = MagicMock()
    client.get_about.return_value = {"data": {"version": "6.4.17"}}
    return client
