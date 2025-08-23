"""Danfoss Link API client.

This module provides a simple wrapper around the Danfoss Link
HTTP API used by the custom component.  It handles authentication,
fetching of rooms, temperatures and set-points, as well as updating
set-points.  Basic rate limiting is included to avoid hammering the
remote service, and several safeguards are in place to surface missing
or malformed responses.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

import requests

_LOGGER = logging.getLogger(__name__)

RATE_LIMIT_SECONDS = 5 * 60  # one call per five minutes


class DanfossLinkApiError(Exception):
    """Base exception for API errors."""


class RateLimitError(DanfossLinkApiError):
    """Raised when the rate limit has been exceeded."""


class DanfossLinkApi:
    """Simple API client for the Danfoss Link system."""

    def __init__(self, base_url: str, username: str, password: str, session: Optional[requests.Session] = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._session = session or requests.Session()
        self._token: Optional[str] = None
        # Track last call time per endpoint to enforce the rate limit.
        self._last_call: Dict[str, float] = {}

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------
    def _check_rate_limit(self, key: str) -> None:
        """Ensure that no more than one call per five minutes is made."""
        last = self._last_call.get(key)
        if last and time.time() - last < RATE_LIMIT_SECONDS:
            raise RateLimitError("API rate limit exceeded: max one call every 5 minutes")
        self._last_call[key] = time.time()

    def _request(self, method: str, path: str, *, key: str, **kwargs: Any) -> Dict[str, Any]:
        """Perform an HTTP request and return the decoded JSON payload.

        The `key` parameter is used for rate limiting.
        """
        self._check_rate_limit(key)
        url = f"{self._base_url}/{path.lstrip('/')}"
        headers = kwargs.pop("headers", {})
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        try:
            response = self._session.request(method, url, headers=headers, timeout=30, **kwargs)
        except requests.RequestException as exc:  # network issues, timeouts, etc.
            raise DanfossLinkApiError("No response from server") from exc

        if response.status_code != 200:
            raise DanfossLinkApiError(f"Unexpected status code {response.status_code}")

        try:
            data = response.json()
        except ValueError as exc:  # JSON decoding error
            raise DanfossLinkApiError("Invalid JSON in response") from exc

        if data is None:
            raise DanfossLinkApiError("Empty response from server")

        return data

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def login(self) -> None:
        """Authenticate against the Danfoss Link system."""
        data = self._request(
            "POST",
            "/login",
            key="login",
            json={"username": self._username, "password": self._password},
        )
        token = data.get("token")
        if not token:
            raise DanfossLinkApiError("Authentication token missing in response")
        self._token = token

    def get_rooms(self) -> List[Dict[str, Any]]:
        """Return a list of available rooms."""
        data = self._request("GET", "/rooms", key="rooms")
        rooms = data.get("rooms")
        if rooms is None:
            raise DanfossLinkApiError("Rooms missing in response")
        return rooms

    def get_temperatures(self) -> Dict[str, float]:
        """Return current temperatures for each room."""
        data = self._request("GET", "/temperatures", key="temperatures")
        temps = data.get("temperatures")
        if temps is None:
            raise DanfossLinkApiError("Temperatures missing in response")
        return temps

    def get_set_points(self) -> Dict[str, float]:
        """Return set-points for each room."""
        data = self._request("GET", "/setpoints", key="setpoints")
        setpoints = data.get("setpoints")
        if setpoints is None:
            raise DanfossLinkApiError("Set-points missing in response")
        return setpoints

    def update_set_point(self, room_id: str, temperature: float) -> None:
        """Update the temperature set-point for a specific room."""
        self._request(
            "PUT",
            f"/rooms/{room_id}/setpoint",
            key=f"update:{room_id}",
            json={"temperature": temperature},
        )
