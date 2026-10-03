import random
import requests

from api.auth.token_manager import TokenManager
from api.config.settings import (
    BASE_URL,
    BROWSE_CATEGORY_ENDPOINT,
    COMMON_HEADERS,
)


class BrowseClient:

    def __init__(self):
        self.token_manager = TokenManager()

    def get_category_response(self, category_id: str) -> requests.Response:
        headers = {
            **COMMON_HEADERS,
            "Accept": "application/vnd.api+json",
            "Authorization": self.token_manager.get_guest_authorization_header(),
            "channelType": "WEB",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        endpoint = BROWSE_CATEGORY_ENDPOINT.format(
            category_id=category_id
        )

        return requests.get(
            url=f"{BASE_URL}{endpoint}",
            headers=headers,
            timeout=20,
        )

    def get_product_ids(self, category_id: str) -> list[str]:
        response = self.get_category_response(category_id)

        response.raise_for_status()

        response_body = response.json()

        products = (
            response_body
            .get("data", {})
            .get("relationships", {})
            .get("products", {})
            .get("data", [])
        )

        product_ids = [
            product["id"]
            for product in products
            if product.get("id")
        ]

        if not product_ids:
            raise RuntimeError(
                f"No products found in category {category_id}"
            )

        return product_ids

    def get_random_product_id(self, category_id: str) -> str:
        product_ids = self.get_product_ids(category_id)

        return random.choice(product_ids)