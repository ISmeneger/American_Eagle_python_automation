import requests

from api.auth.token_manager import TokenManager
from api.config.settings import (
    BASE_URL,
    COMMON_HEADERS,
    INVENTORY_ENDPOINT,
)


class InventoryClient:

    def __init__(self):
        self.token_manager = TokenManager()

    def get_inventory_response(self, product_id: str) -> requests.Response:
        headers = {
            **COMMON_HEADERS,
            "Authorization": self.token_manager.get_guest_authorization_header(),
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        endpoint = INVENTORY_ENDPOINT.format(
            product_id=product_id
        )

        return requests.get(
            url=f"{BASE_URL}{endpoint}",
            headers=headers,
            timeout=20,
        )

    def get_available_skus(self, product_id: str) -> list[str]:
        response = self.get_inventory_response(product_id)

        response.raise_for_status()

        response_body = response.json()

        inventory_items = (
            response_body
            .get("data", {})
            .get(product_id, [])
        )

        available_skus = [
            item["skuId"]
            for item in inventory_items
            if item.get("skuId")
               and item.get("inventoryLevel", 0) > 0
        ]

        return available_skus