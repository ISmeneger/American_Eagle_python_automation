import requests

from api.auth.token_manager import TokenManager
from api.config.settings import (
    BASE_URL,
    BAG_ENDPOINT,
    BAG_ITEMS_ENDPOINT,
    COMMON_HEADERS,
)


class BagClient:

    def __init__(self):
        self.token_manager = TokenManager()

    def get_bag_response(self) -> requests.Response:
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

        return requests.get(
            url=f"{BASE_URL}{BAG_ENDPOINT}",
            headers=headers,
            timeout=20,
        )

    def add_item(
            self,
            sku_id: str,
            quantity: int = 1,
    ) -> requests.Response:
        headers = {
            **COMMON_HEADERS,
            "Authorization": self.token_manager.get_guest_authorization_header(),
            "Content-Type": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        payload = {
            "items": [
                {
                    "skuId": sku_id,
                    "quantity": quantity,
                }
            ]
        }

        return requests.post(
            url=f"{BASE_URL}{BAG_ITEMS_ENDPOINT}",
            headers=headers,
            json=payload,
            timeout=20,
        )

    def update_item(
            self,
            item_id: str,
            sku_id: str,
            quantity: int,
    ) -> requests.Response:
        headers = {
            **COMMON_HEADERS,
            "Authorization": self.token_manager.get_guest_authorization_header(),
            "Content-Type": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        payload = {
            "items": [
                {
                    "skuId": sku_id,
                    "quantity": quantity,
                    "itemId": item_id,
                }
            ]
        }

        return requests.patch(
            url=f"{BASE_URL}{BAG_ITEMS_ENDPOINT}",
            headers=headers,
            json=payload,
            timeout=20,
        )

    def delete_item(
            self,
            item_id: str,
    ) -> requests.Response:
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

        return requests.delete(
            url=f"{BASE_URL}{BAG_ITEMS_ENDPOINT}",
            headers=headers,
            params={
                "itemIds": item_id,
            },
            timeout=20,
        )