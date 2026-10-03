from api.config.settings import TEST_CATEGORY_ID
from utils.test_data_helper import get_available_product_skus


def test_bag_item_lifecycle(
    browse_client,
    inventory_client,
    bag_client,
):
    bag_response = bag_client.get_bag_response()

    assert bag_response.status_code == 200

    bag_body = bag_response.json()

    assert bag_body["data"]["itemCount"] == 0

    candidates = get_available_product_skus(
        browse_client,
        inventory_client,
        TEST_CATEGORY_ID,
    )

    added_product_id = None
    added_sku_id = None
    add_response = None

    for product_id, sku_id in candidates:
        print(
            f"\nTrying Product ID: {product_id}, "
            f"SKU ID: {sku_id}"
        )

        add_response = bag_client.add_item(
            sku_id=sku_id,
            quantity=1,
        )

        print("Add item status:", add_response.status_code)

        if add_response.status_code == 202:
            added_product_id = product_id
            added_sku_id = sku_id
            break

        if add_response.status_code == 422:
            response_body = add_response.json()

            errors = response_body.get("errors", [])

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

    assert added_sku_id is not None, (
        "Could not find a SKU that can be added to the bag"
    )

    print("\nAdded Product ID:", added_product_id)
    print("Added SKU ID:", added_sku_id)

    updated_bag_response = bag_client.get_bag_response()

    assert updated_bag_response.status_code == 200

    updated_bag = updated_bag_response.json()

    assert updated_bag["data"]["itemCount"] == 1

    items = updated_bag["data"]["items"]

    assert len(items) == 1

    added_item = items[0]

    assert added_item["sku"] == added_sku_id
    assert added_item["productId"] == added_product_id
    assert added_item["quantity"] == 1
    assert added_item["available"] is True
    assert added_item["productName"]
    assert added_item["size"]
    assert added_item["originalPrice"] > 0
    assert added_item["price"] > 0

    item_id = added_item["itemId"]

    update_response = bag_client.update_item(
        item_id=item_id,
        sku_id=added_sku_id,
        quantity=2,
    )

    print("Update item status:", update_response.status_code)
    print("Update item response:", update_response.text)

    assert update_response.status_code == 202

    updated_bag_response = bag_client.get_bag_response()

    assert updated_bag_response.status_code == 200

    updated_bag = updated_bag_response.json()

    updated_item = updated_bag["data"]["items"][0]

    assert updated_item["sku"] == added_sku_id
    assert updated_item["quantity"] == 2

    delete_response = bag_client.delete_item(
        item_id=item_id,
    )

    print("Delete item status:", delete_response.status_code)
    print("Delete item response:", delete_response.text)

    assert delete_response.status_code == 202

    final_bag_response = bag_client.get_bag_response()

    assert final_bag_response.status_code == 200

    final_bag = final_bag_response.json()

    assert final_bag["data"]["itemCount"] == 0
    assert final_bag["data"]["items"] == []
