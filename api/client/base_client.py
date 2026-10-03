import requests

from api.auth.token_manager import TokenManager
from api.config.settings import COMMON_HEADERS


class BaseClient:

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )

    def __init__(self):
        self.token_manager = TokenManager()
        self.session = requests.Session()

        self.session.headers.update(
            {
                **COMMON_HEADERS,
                "User-Agent": self.USER_AGENT,
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    def get_headers(
        self,
        content_type: str | None = None,
        accept: str | None = None,
    ) -> dict[str, str]:

        headers = {
            "Authorization":
                self.token_manager.get_guest_authorization_header(),
        }

        if content_type:
            headers["Content-Type"] = content_type

        if accept:
            headers["Accept"] = accept

        return headers