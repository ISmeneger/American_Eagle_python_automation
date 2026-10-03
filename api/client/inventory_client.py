import requests

from api.client.base_client import BaseClient
from api.config.settings import (
    BASE_URL,
    INVENTORY_ENDPOINT,
)


class InventoryClient(BaseClient):

    def get_inventory_response(
        self,
        product_id: str,
    ) -> requests.Response:

        endpoint = INVENTORY_ENDPOINT.format(
            product_id=product_id
        )

        return requests.get(
            url=f"{BASE_URL}{endpoint}",
            headers=self.get_headers(),
            timeout=20,
        )

    def get_available_skus(
        self,
        product_id: str,
    ) -> list[str]:

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