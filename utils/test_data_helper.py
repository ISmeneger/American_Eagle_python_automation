import random


def get_available_product_skus(
    browse_client,
    inventory_client,
    category_id: str,
) -> list[tuple[str, str]]:

    product_ids = browse_client.get_product_ids(category_id)

    random.shuffle(product_ids)

    candidates = []

    for product_id in product_ids:
        available_skus = inventory_client.get_available_skus(product_id)

        random.shuffle(available_skus)

        for sku_id in available_skus:
            candidates.append((product_id, sku_id))

    if not candidates:
        raise RuntimeError(
            f"No available products found in category {category_id}"
        )

    return candidates