from api.config.settings import TEST_CATEGORY_ID
from utils.test_data_helper import get_available_product_skus


def test_get_available_product_and_sku(
    browse_client,
    inventory_client,
):
    candidates = get_available_product_skus(
        browse_client,
        inventory_client,
        TEST_CATEGORY_ID,
    )

    assert candidates

    product_id, sku_id = candidates[0]

    print("\nProduct ID:", product_id)
    print("SKU ID:", sku_id)

    assert product_id
    assert sku_id