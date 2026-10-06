import allure
import pytest

from api.config.settings import TEST_CATEGORY_ID
from utils.test_data_helper import get_available_product_skus


pytestmark = [
    pytest.mark.api,
    pytest.mark.bag,
]


@pytest.mark.smoke
@pytest.mark.positive
@allure.feature("Bag API")
@allure.story("Bag item lifecycle")
@allure.title("Add, update and delete item in guest bag")
def test_bag_item_lifecycle(
    browse_client,
    inventory_client,
    bag_client,
    clean_bag,
):
    with allure.step("Get empty guest bag"):
        bag_response = bag_client.get_bag_response()

        assert bag_response.status_code == 200

        bag_body = bag_response.json()

        assert bag_body["data"]["itemCount"] == 0

    with allure.step("Find available product and SKU"):
        candidates = get_available_product_skus(
            browse_client,
            inventory_client,
            TEST_CATEGORY_ID,
        )

    with allure.step("Add available item to bag"):
        added_product_id = None
        added_sku_id = None

        for product_id, sku_id in candidates:
            add_response = bag_client.add_item(
                sku_id=sku_id,
                quantity=1,
            )

            if add_response.status_code == 202:
                added_product_id = product_id
                added_sku_id = sku_id
                break

            if add_response.status_code == 422:
                errors = add_response.json().get("errors", [])

                if any(
                        error.get("key")
                        == "error.cart.item.skuItem.out_of_stock"
                        for error in errors
                ):
                    continue

            raise AssertionError(
                f"Unexpected add item response: "
                f"{add_response.status_code} {add_response.text}"
            )

        assert added_sku_id is not None

    with allure.step("Verify item was added to bag"):
        updated_bag_response = bag_client.get_bag_response()

        assert updated_bag_response.status_code == 200

        updated_bag = updated_bag_response.json()

        assert updated_bag["data"]["itemCount"] == 1

        added_item = updated_bag["data"]["items"][0]

        assert added_item["sku"] == added_sku_id
        assert added_item["productId"] == added_product_id
        assert added_item["quantity"] == 1
        assert added_item["available"] is True
        assert added_item["productName"]
        assert added_item["size"]
        assert added_item["originalPrice"] > 0
        assert added_item["price"] > 0

        item_id = added_item["itemId"]

    with allure.step("Update item quantity from 1 to 2"):
        update_response = bag_client.update_item(
            item_id=item_id,
            sku_id=added_sku_id,
            quantity=2,
        )

        assert update_response.status_code == 202

        updated_bag_response = bag_client.get_bag_response()

        assert updated_bag_response.status_code == 200

        updated_item = (
            updated_bag_response
            .json()["data"]["items"][0]
        )

        assert updated_item["sku"] == added_sku_id
        assert updated_item["quantity"] == 2

    with allure.step("Delete item from bag"):
        delete_response = bag_client.delete_item(
            item_id=item_id,
        )

        assert delete_response.status_code == 202

    with allure.step("Verify bag is empty"):
        final_bag_response = bag_client.get_bag_response()

        assert final_bag_response.status_code == 200

        final_bag = final_bag_response.json()

        assert final_bag["data"]["itemCount"] == 0
        assert final_bag["data"]["items"] == []


@pytest.mark.positive
@allure.feature("Bag API")
@allure.story("Multiple bag items")
@allure.title("Add multiple different items to guest bag")
def test_add_multiple_different_items_to_bag(
    browse_client,
    inventory_client,
    bag_client,
    clean_bag,
):
    with allure.step("Get available product candidates"):
        candidates = get_available_product_skus(
            browse_client,
            inventory_client,
            TEST_CATEGORY_ID,
        )

    added_skus = set()

    with allure.step("Add two different available SKUs to bag"):
        for product_id, sku_id in candidates:
            if sku_id in added_skus:
                continue

            response = bag_client.add_item(
                sku_id=sku_id,
                quantity=1,
            )

            if response.status_code == 422:
                response_body = response.json()
                errors = response_body.get("errors", [])

                if (
                    errors
                    and errors[0].get("key")
                    == "error.cart.item.skuItem.out_of_stock"
                ):
                    continue

            assert response.status_code == 202

            added_skus.add(sku_id)

            if len(added_skus) == 2:
                break

    assert len(added_skus) == 2, (
        "Could not add two different available SKUs to bag"
    )

    with allure.step("Get bag after adding two items"):
        response = bag_client.get_bag_response()

        assert response.status_code == 200

        bag = response.json()

    with allure.step("Verify two different items are present in bag"):
        items = bag["data"]["items"]

        bag_skus = {
            item["sku"]
            for item in items
        }

        assert len(items) == 2
        assert added_skus == bag_skus

        for item in items:
            assert item["quantity"] == 1
            assert item["itemId"]
            assert item["productId"]
            assert item["productName"]
            assert item["sku"]


@pytest.mark.negative
@allure.feature("Bag API")
@allure.story("Bag negative scenarios")
@allure.title("Add item to bag without Bearer token")
def test_add_item_without_authorization(
    browse_client,
    inventory_client,
    bag_client,
    clean_bag,
):
    candidates = get_available_product_skus(
        browse_client,
        inventory_client,
        TEST_CATEGORY_ID,
    )

    product_id, sku_id = candidates[0]

    with allure.step("Add valid SKU without Authorization"):
        response = bag_client.add_item(
            sku_id=sku_id,
            quantity=1,
            include_authorization=False,
        )

    with allure.step("Verify 401 response without Bearer token"):
        assert response.status_code == 401

        response_body = response.json()

        assert response_body["error"]["status"] == "401"

        error = response_body["error"]["errors"][0]

        assert error["key"] == "apicg.token.invalid"


@pytest.mark.negative
@allure.feature("Bag API")
@allure.story("Bag negative scenarios")
@allure.title("Add invalid SKU to bag")
def test_add_invalid_sku(
    bag_client,
    clean_bag,
):
    invalid_sku_id = "9999999999"

    with allure.step("Add invalid SKU"):
        response = bag_client.add_item(
            sku_id=invalid_sku_id,
            quantity=1,
        )

    with allure.step("Verify 422 response for invalid SKU"):
        assert response.status_code == 422

        response_body = response.json()

        error = response_body["errors"][0]

        assert error["key"] == "error.cart.general"
        assert error["message"] == "SKU is Invalid"
        assert "skuId" in error["fields"]
        assert invalid_sku_id in error["args"][0]


@pytest.mark.negative
@allure.feature("Bag API")
@allure.story("Bag negative scenarios")
@allure.title("Delete nonexistent item from bag")
def test_delete_nonexistent_item(
    bag_client,
    clean_bag,
):
    invalid_item_id = "00000000-0000-0000-0000-000000000000"

    with allure.step("Delete nonexistent item"):
        response = bag_client.delete_item(
            item_id=invalid_item_id,
        )

    with allure.step("Verify 404 response for nonexistent item"):
        assert response.status_code == 404

        response_body = response.json()

        assert response_body["status"] == 404
        assert response_body["errorName"] == "CartNotFoundException"

        error = response_body["errors"][0]

        assert error["status"] == "404"
        assert error["key"] == "error.cart.notFound"
        assert error["message"] == "Cart Not Found"
        assert "cartId" in error["fields"]


@pytest.mark.negative
@allure.feature("Bag API")
@allure.story("Bag negative scenarios")
@allure.title("Update item quantity to zero")
def test_update_item_with_zero_quantity(
    browse_client,
    inventory_client,
    bag_client,
    clean_bag,
):
    candidates = get_available_product_skus(
        browse_client,
        inventory_client,
        TEST_CATEGORY_ID,
    )

    added_item = None

    with allure.step("Add available item to bag"):
        for product_id, sku_id in candidates:
            response = bag_client.add_item(
                sku_id=sku_id,
                quantity=1,
            )

            if response.status_code == 422:
                response_body = response.json()
                errors = response_body.get("errors", [])

                if (
                    errors
                    and errors[0].get("key")
                    == "error.cart.item.skuItem.out_of_stock"
                ):
                    continue

            assert response.status_code == 202

            bag_response = bag_client.get_bag_response()

            assert bag_response.status_code == 200

            items = bag_response.json()["data"]["items"]

            added_item = next(
                item
                for item in items
                if item["sku"] == sku_id
            )

            break

    assert added_item is not None

    with allure.step("Update item quantity to zero"):
        response = bag_client.update_item(
            sku_id=added_item["sku"],
            quantity=0,
            item_id=added_item["itemId"],
        )

    with allure.step("Verify 400 response for zero quantity"):
        assert response.status_code == 400

        response_body = response.json()

        assert response_body["status"] == 400
        assert (
                response_body["errorName"]
                == "HandlerMethodValidationException"
        )

        error = response_body["errors"][0]

        assert error["status"] == "400"
        assert error["key"] == "error.cart.general"
        assert error["message"] == "error.cart.item_qty_invalid"
        assert "items[0].quantity" in error["fields"]
        assert 0 in error["args"]