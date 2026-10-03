from api.client.browse_client import BrowseClient
from api.client.inventory_client import InventoryClient
from api.config.settings import TEST_CATEGORY_ID
from utils.test_data_helper import get_random_available_product_and_sku


def test_get_available_product_and_sku():
    browse_client = BrowseClient()
    inventory_client = InventoryClient()

    product_id, sku_id = get_random_available_product_and_sku(
        browse_client,
        inventory_client,
        TEST_CATEGORY_ID,
    )

    print("\nProduct ID:", product_id)
    print("SKU ID:", sku_id)

    assert product_id
    assert sku_id