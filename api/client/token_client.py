import requests

from api.config.settings import (
    BASE_URL,
    COMMON_HEADERS,
    GUEST_TOKEN_ENDPOINT,
    get_guest_auth,
)


class TokenClient:

    def __init__(self, session: requests.Session | None = None):
        self.session = session or requests.Session()

    def get_guest_token_response(self) -> requests.Response:
        headers = {
            **COMMON_HEADERS,
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": get_guest_auth(),
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        data = {
            "grant_type": "client_credentials",
        }

        return self.session.post(
            url=f"{BASE_URL}{GUEST_TOKEN_ENDPOINT}",
            headers=headers,
            data=data,
            timeout=20,
        )

    def get_guest_token(self) -> str:
        response = self.get_guest_token_response()

        response.raise_for_status()

        token = response.json().get("access_token")

        if not token:
            raise RuntimeError(
                "Guest access token was not returned by API"
            )

        return token