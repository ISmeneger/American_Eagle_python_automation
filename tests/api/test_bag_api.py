import allure

from api.config.settings import TEST_CATEGORY_ID
from utils.test_data_helper import get_available_product_skus

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
