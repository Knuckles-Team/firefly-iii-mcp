from typing import Any

import requests


class ApiClientBase:
    """Base HTTP API client wrapper."""

    def __init__(self, base_url: str, token: str, verify: bool = True):
        base_url = base_url.rstrip("/")
        # Firefly III mounts its REST API under /api; tolerate a base URL given
        # with or without the suffix.
        if not base_url.endswith("/api"):
            base_url = f"{base_url}/api"
        self.base_url = base_url
        self.token = token
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, verify=self.verify, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"status": response.status_code, "text": response.text}
