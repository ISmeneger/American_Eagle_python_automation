import requests

from api.client.base_client import BaseClient
from api.config.settings import (
    BASE_URL,
    BAG_ENDPOINT,
    BAG_ITEMS_ENDPOINT,
)


class BagClient(BaseClient):

    def get_bag_response(self) -> requests.Response:
        return requests.get(
            url=f"{BASE_URL}{BAG_ENDPOINT}",
            headers=self.get_headers(),
            timeout=20,
        )

    def add_item(
        self,
        sku_id: str,
        quantity: int = 1,
    ) -> requests.Response:

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
            headers=self.get_headers(
                content_type="application/json"
            ),
            json=payload,
            timeout=20,
        )

    def update_item(
        self,
        item_id: str,
        sku_id: str,
        quantity: int,
    ) -> requests.Response:

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
            headers=self.get_headers(
                content_type="application/json"
            ),
            json=payload,
            timeout=20,
        )

    def delete_item(
        self,
        item_id: str,
    ) -> requests.Response:

        return requests.delete(
            url=f"{BASE_URL}{BAG_ITEMS_ENDPOINT}",
            headers=self.get_headers(),
            params={
                "itemIds": item_id,
            },
            timeout=20,
        )