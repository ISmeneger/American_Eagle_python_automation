import allure
import pytest

from api.config.settings import TEST_CATEGORY_ID
from utils.test_data_helper import get_available_product_skus


pytestmark = [
    pytest.mark.api,
    pytest.mark.inventory,
]


@pytest.mark.smoke
@pytest.mark.positive
@allure.feature("Inventory API")
@allure.story("Product availability")
@allure.title("Get available SKU for product")
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


@pytest.mark.negative
@allure.feature("Inventory API")
@allure.story("Inventory negative scenarios")
@allure.title("Request inventory for invalid product")
def test_get_inventory_for_invalid_product(inventory_client):
    invalid_product_id = "invalid_product_id"

    with allure.step("Request inventory for invalid product"):
        response = inventory_client.get_inventory_response(
            invalid_product_id
        )

    with allure.step("Verify empty inventory response"):
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["data"] == {}
        assert response_body["error"] is None


@pytest.mark.negative
@allure.feature("Inventory API")
@allure.story("Inventory negative scenarios")
@allure.title("Request inventory without Bearer token")
def test_get_inventory_without_authorization(
    browse_client,
    inventory_client,
):
    with allure.step("Get valid product from test category"):
        product_id = browse_client.get_random_product_id(
            TEST_CATEGORY_ID
        )

    with allure.step("Request inventory without Authorization"):
        response = inventory_client.get_inventory_response(
            product_id,
            include_authorization=False,
        )

    with allure.step("Verify 401 response without Bearer token"):
        assert response.status_code == 401

        response_body = response.json()

        assert response_body["error"]["status"] == "401"

        error = response_body["error"]["errors"][0]

        assert error["key"] == "apicg.token.invalid"