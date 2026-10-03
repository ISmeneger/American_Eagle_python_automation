import allure

from api.client.browse_client import BrowseClient
from api.config.settings import TEST_CATEGORY_ID

@allure.feature("Browse API")
@allure.story("Category products")
@allure.title("Get products from category")
def test_get_products_from_category():
    browse_client = BrowseClient()

    response = browse_client.get_category_response(TEST_CATEGORY_ID)

    assert response.status_code == 200

    product_ids = browse_client.get_product_ids(TEST_CATEGORY_ID)

    assert product_ids
    assert len(product_ids) > 0

def test_get_random_product_id():
    browse_client = BrowseClient()

    product_id = browse_client.get_random_product_id(
        TEST_CATEGORY_ID
    )

    assert product_id
    print("\nRandom product ID:", product_id)