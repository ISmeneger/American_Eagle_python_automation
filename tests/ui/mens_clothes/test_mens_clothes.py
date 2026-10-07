from decimal import Decimal

import allure
import pytest

from ui.config import BASE_URL
from ui.constants import (
    MEN_PATH,
    MENS_CLOTHES_TITLE,
)
from ui.pages.home_page import HomePage
from ui.pages.mens_clothes_page import MensClothesPage


pytestmark = [
    pytest.mark.ui,
    pytest.mark.positive,
]


@allure.feature("Men's Clothes")
@allure.story("Men's catalog")
@allure.title("Open Men's Clothes page")
def test_mens_clothes_page_opens_correctly(driver):
    home_page = HomePage(driver)
    mens_clothes_page = MensClothesPage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Open Men's menu"):
        mens_clothes_page.move_to_men_menu()

    with allure.step("Click View All in Men's menu"):
        mens_clothes_page.click_view_all_categories()

    with allure.step("Close popup if available"):
        mens_clothes_page.close_popup_if_available()

    with allure.step("Verify Men's Clothes page title"):
        assert (
            mens_clothes_page.get_mens_page_title()
            == MENS_CLOTHES_TITLE
        )

    with allure.step("Verify Men's Clothes page URL"):
        assert (
            mens_clothes_page.get_current_url()
            == BASE_URL.rstrip("/") + MEN_PATH
        )


@allure.feature("Men's Clothes")
@allure.story("Product sorting")
@allure.title("Sort products by price from low to high")
def test_products_are_sorted_by_price_low_to_high(
    home_page,
    mens_clothes_page,
):
    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Open Men's Clothes catalog"):
        mens_clothes_page.move_to_men_menu()
        mens_clothes_page.click_view_all_categories()
        mens_clothes_page.close_popup_if_available()

    with allure.step("Sort products by Price: Low to High"):
        mens_clothes_page.select_price_low_to_high()

    with allure.step("Get product prices"):
        prices = mens_clothes_page.get_product_prices()

    with allure.step(
        "Verify products are sorted by price from low to high"
    ):
        assert len(prices) > 1

        assert prices == sorted(prices)


@allure.feature("Men's Clothes")
@allure.story("Product filtering")
@allure.title("Filter products by price from $25 to $50")
def test_products_are_filtered_by_price_25_to_50(
    home_page,
    mens_clothes_page,
):
    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Open Men's Clothes catalog"):
        mens_clothes_page.move_to_men_menu()
        mens_clothes_page.click_view_all_categories()
        mens_clothes_page.close_popup_if_available()

    with allure.step("Select price filter from $25 to $50"):
        mens_clothes_page.select_price_filter_25_to_50()

    with allure.step("Wait for filtered product prices"):
        mens_clothes_page.wait.until(
            lambda driver:
            all(
                Decimal("25.00")
                <= price
                <= Decimal("50.00")
                for price in mens_clothes_page.get_product_prices()
            )
        )

    with allure.step("Get filtered product prices"):
        prices = mens_clothes_page.get_product_prices()

    with allure.step(
            "Verify all product prices are between $25 and $50"
    ):
        assert prices

        assert all(
            Decimal("25.00")
            <= price
            <= Decimal("50.00")
            for price in prices
        )
