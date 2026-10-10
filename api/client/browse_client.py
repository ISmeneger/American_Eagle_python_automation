import random

import requests

from api.client.base_client import BaseClient
from api.config.settings import (
    BASE_URL,
    BROWSE_CATEGORY_ENDPOINT,
)


class BrowseClient(BaseClient):

    def get_category_response(
            self,
            category_id: str,
            include_authorization: bool = True,
            offset: int = 0,
            rows: int = 30,
    ) -> requests.Response:

        if include_authorization:
            headers = self.get_headers(
                accept="application/vnd.api+json"
            )
        else:
            headers = {
                "Accept": "application/vnd.api+json",
            }

        headers["channelType"] = "WEB"

        endpoint = BROWSE_CATEGORY_ENDPOINT.format(
            category_id=category_id
        )

        return self.session.get(
            url=f"{BASE_URL}{endpoint}",
            headers=headers,
            params={
                "offset": offset,
                "rows": rows,
            },
            timeout=20,
        )

    def get_product_ids(
            self,
            category_id: str,
            pages: int = 3,
            rows: int = 30,
    ) -> list[str]:

        product_ids = []

        for page in range(pages):
            offset = page * rows

            response = self.get_category_response(
                category_id=category_id,
                offset=offset,
                rows=rows,
            )

            response.raise_for_status()

            response_body = response.json()

            products = (
                response_body
                .get("data", {})
                .get("relationships", {})
                .get("products", {})
                .get("data", [])
            )

            page_product_ids = [
                product["id"]
                for product in products
                if product.get("id")
            ]

            product_ids.extend(page_product_ids)

            if len(page_product_ids) < rows:
                break

        if not product_ids:
            raise RuntimeError(
                f"No products found in category {category_id}"
            )

        return product_ids

    def get_random_product_id(
        self,
        category_id: str,
    ) -> str:

        product_ids = self.get_product_ids(category_id)

        return random.choice(product_ids)