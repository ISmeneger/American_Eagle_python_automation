from decimal import Decimal, ROUND_CEILING

import allure
import pytest

from ui.constants import (
    ADDED_TO_BAG_MESSAGE,
    EMPTY_BAG_MESSAGE,
    FREE_SHIPPING_THRESHOLD,
    MAX_ALLOWED_QUANTITY,
    ONE_ITEM_TEXT,
    TWO_ITEMS_TEXT,
)


pytestmark = [
    pytest.mark.ui,
    pytest.mark.positive,
]


@allure.feature("Men's Clothes")
@allure.story("Product and Bag")
@allure.title("Add item from catalog to bag")
def test_add_item_from_catalog_to_bag(
    product_cart_steps,
    product_page,
):
    with allure.step("Add first Men's product to bag"):
        product_cart_steps.add_first_mens_product_to_bag()

    with allure.step("Verify Added to bag message"):
        assert (
            product_page.get_added_to_bag_message()
            == ADDED_TO_BAG_MESSAGE
        )


@allure.feature("Men's Clothes")
@allure.story("Product and Bag")
@allure.title("Product price matches price in Shopping Bag")
def test_product_price_matches_cart_price(
    product_cart_steps,
    product_page,
    cart_page,
):
    with allure.step("Add first Men's product to bag"):
        product = (
            product_cart_steps
            .add_first_mens_product_to_bag()
        )

    with allure.step("Open Shopping Bag"):
        product_page.open_shopping_bag()

    with allure.step("Get product price in Shopping Bag"):
        cart_price = Decimal(
            cart_page
            .get_product_price_in_cart()
            .replace("$", "")
            .strip()
        )

    with allure.step(
        "Verify product price matches Shopping Bag price"
    ):
        assert cart_price == product["price"]


@allure.feature("Men's Clothes")
@allure.story("Product and Bag")
@allure.title("Selected product size matches size in Shopping Bag")
def test_selected_product_size_matches_cart_size(
    product_cart_steps,
    product_page,
    cart_page,
):
    with allure.step("Add first Men's product to bag"):
        product = (
            product_cart_steps
            .add_first_mens_product_to_bag()
        )

    with allure.step("Open Shopping Bag"):
        product_page.open_shopping_bag()

    with allure.step("Get product size in Shopping Bag"):
        cart_size = cart_page.get_product_size()

    with allure.step(
        "Verify selected size matches Shopping Bag size"
    ):
        assert cart_size == product["size"]


@allure.feature("Men's Clothes")
@allure.story("Product and Bag")
@allure.title("Change product quantity in Shopping Bag and verify subtotal")
def test_change_product_quantity_and_verify_subtotal(
    product_cart_steps,
    product_page,
    cart_page,
):
    with allure.step("Add first Men's product to bag"):
        product = (
            product_cart_steps
            .add_first_mens_product_to_bag()
        )

    with allure.step("Open Shopping Bag"):
        product_page.open_shopping_bag()

    with allure.step("Verify Shopping Bag contains one item"):
        assert (
            cart_page.get_quantity_of_items_text()
            == ONE_ITEM_TEXT
        )

    with allure.step("Open product editing"):
        cart_page.click_edit_item_button()

    with allure.step("Move to Update Bag button"):
        cart_page.move_to_update_bag_button()

    with allure.step("Increase product quantity"):
        cart_page.increase_product_quantity()

    with allure.step("Update Shopping Bag"):
        cart_page.update_bag()

    with allure.step("Verify Shopping Bag contains two items"):
        assert (
            cart_page.get_quantity_of_items_text()
            == TWO_ITEMS_TEXT
        )

    with allure.step("Calculate expected subtotal"):
        expected_subtotal = product["price"] * 2

    with allure.step(
        "Wait for Shopping Bag subtotal to be recalculated"
    ):
        subtotal_text = cart_page.wait_for_subtotal(
            f"${expected_subtotal:.2f}"
        )

    with allure.step("Verify subtotal"):
        subtotal = Decimal(
            subtotal_text
            .replace("$", "")
            .strip()
        )

        assert subtotal == expected_subtotal


@allure.feature("Men's Clothes")
@allure.story("Product and Bag")
@allure.title("Free Shipping is displayed when cart reaches threshold")
def test_free_shipping_is_displayed_when_threshold_is_reached(
    product_cart_steps,
    product_page,
    cart_page,
):
    with allure.step("Add first Men's product to bag"):
        product = (
            product_cart_steps
            .add_first_mens_product_to_bag()
        )

    with allure.step("Open Shopping Bag"):
        product_page.open_shopping_bag()

    with allure.step("Calculate quantity required for Free Shipping"):
        required_quantity = int(
            (
                FREE_SHIPPING_THRESHOLD
                / product["price"]
            ).to_integral_value(
                rounding=ROUND_CEILING
            )
        )

    if required_quantity > 1:
        with allure.step("Open product editing"):
            cart_page.click_edit_item_button()

        with allure.step("Move to Update Bag button"):
            cart_page.move_to_update_bag_button()

        with allure.step(
            f"Increase product quantity to {required_quantity}"
        ):
            for _ in range(required_quantity - 1):
                cart_page.increase_product_quantity()

        with allure.step("Update Shopping Bag"):
            cart_page.update_bag()

        expected_subtotal = (
            product["price"]
            * required_quantity
        )

        with allure.step(
            "Wait for Shopping Bag subtotal to be recalculated"
        ):
            cart_page.wait_for_subtotal(
                f"${expected_subtotal:.2f}"
            )

    with allure.step(
        "Verify Free Shipping message is displayed"
    ):
        assert cart_page.is_free_shipping_message_displayed()


@allure.feature("Men's Clothes")
@allure.story("Product and Bag")
@allure.title("Maximum product quantity in Shopping Bag is 10")
def test_maximum_product_quantity_in_cart(
    product_cart_steps,
    product_page,
    cart_page,
):
    with allure.step("Add first Men's product to bag"):
        product_cart_steps.add_first_mens_product_to_bag()

    with allure.step("Open Shopping Bag"):
        product_page.open_shopping_bag()

    with allure.step("Open product editing"):
        cart_page.click_edit_item_button()

    with allure.step("Move to Update Bag button"):
        cart_page.move_to_update_bag_button()

    with allure.step(
        "Increase product quantity until increase button is disabled"
    ):
        maximum_quantity = (
            cart_page.increase_quantity_until_disabled()
        )

    with allure.step("Verify maximum allowed quantity"):
        assert maximum_quantity == MAX_ALLOWED_QUANTITY

    with allure.step(
        "Verify increase quantity button is disabled"
    ):
        assert not cart_page.is_increase_quantity_button_enabled()


@allure.feature("Men's Clothes")
@allure.story("Product and Bag")
@allure.title("Remove product from Shopping Bag")
def test_remove_product_from_cart(
    product_cart_steps,
    product_page,
    cart_page,
):
    with allure.step("Add first Men's product to bag"):
        product_cart_steps.add_first_mens_product_to_bag()

    with allure.step("Open Shopping Bag"):
        product_page.open_shopping_bag()

    with allure.step("Verify product is displayed in Shopping Bag"):
        assert cart_page.get_product_name().strip()

    with allure.step("Remove product from Shopping Bag"):
        cart_page.remove_product_from_bag()

    with allure.step("Verify Shopping Bag is empty"):
        assert (
            cart_page.get_empty_bag_message()
            == EMPTY_BAG_MESSAGE
        )


@allure.feature("Men's Clothes")
@allure.story("Multiple products in Shopping Bag")
@allure.title("Add two different products to Shopping Bag")
def test_two_different_products_in_cart(
    home_page,
    product_cart_steps,
    product_page,
    cart_page,
):
    with allure.step("Add first Men's product to bag"):
        first_product = (
            product_cart_steps
            .add_first_mens_product_to_bag()
        )

    with allure.step("Return to American Eagle home page"):
        home_page.open(close_overlays=False)

    with allure.step("Add first Jeans product to bag"):
        second_product = (
            product_cart_steps
            .add_first_jeans_product_to_bag()
        )

    with allure.step("Open Shopping Bag"):
        product_page.open_shopping_bag()

    with allure.step("Verify Shopping Bag contains two items"):
        assert (
            cart_page.get_quantity_of_items_text()
            == TWO_ITEMS_TEXT
        )

    with allure.step("Get Shopping Bag items"):
        cart_items = cart_page.get_cart_items()

        assert len(cart_items) == 2

        cart_items_by_name = {
            item["name"]: item
            for item in cart_items
        }

    with allure.step("Verify first product"):
        assert first_product["name"] in cart_items_by_name

        first_cart_item = (
            cart_items_by_name[
                first_product["name"]
            ]
        )

        assert (
            first_cart_item["size"]
            == first_product["size"]
        )

        assert (
            first_cart_item["price"]
            == first_product["price"]
        )

    with allure.step("Verify second product"):
        assert second_product["name"] in cart_items_by_name

        second_cart_item = (
            cart_items_by_name[
                second_product["name"]
            ]
        )

        assert (
            second_cart_item["size"]
            == second_product["size"]
        )

        assert (
            second_cart_item["price"]
            == second_product["price"]
        )

    with allure.step("Verify Shopping Bag subtotal"):
        expected_subtotal = (
            first_product["price"]
            + second_product["price"]
        )

        subtotal_text = (
            cart_page.wait_for_subtotal(
                f"${expected_subtotal:.2f}"
            )
        )

        subtotal = Decimal(
            subtotal_text
            .replace("$", "")
            .strip()
        )

        assert subtotal == expected_subtotal
