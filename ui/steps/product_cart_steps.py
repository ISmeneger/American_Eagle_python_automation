from decimal import Decimal

from ui.pages.jeans_page import JeansPage
from ui.pages.product_page import ProductPage
from ui.steps.product_catalog_steps import ProductCatalogSteps


class ProductCartSteps:
    def __init__(self, driver):
        self.product_catalog_steps = ProductCatalogSteps(driver)
        self.jeans_page = JeansPage(driver)
        self.product_page = ProductPage(driver)

    def open_first_mens_product(self) -> dict:
        product_name = (
            self.product_catalog_steps
            .open_first_available_mens_product()
        )

        self.product_page.close_popup_if_available()

        product_price = Decimal(
            self.product_page
            .get_product_price()
            .replace("Now", "")
            .replace("$", "")
            .strip()
        )

        return {
            "name": product_name,
            "price": product_price,
        }

    def select_size_and_add_to_bag(self) -> str:
        self.product_page.select_first_available_size()

        selected_size = (
            self.product_page.get_selected_size()
        )

        self.product_page.click_add_to_bag_button()

        return selected_size

    def add_first_mens_product_to_bag(self) -> dict:
        product_data = self.open_first_mens_product()

        product_data["size"] = (
            self.select_size_and_add_to_bag()
        )

        return product_data

    def add_first_jeans_product_to_bag(self) -> dict:
        self.jeans_page.move_to_jeans_menu()
        self.jeans_page.click_mens_view_all()
        self.jeans_page.close_popup_if_available()

        product_name = (
            self.jeans_page
            .open_first_available_product()
        )

        self.product_page.close_popup_if_available()

        product_price = Decimal(
            self.product_page
            .get_product_price()
            .replace("Now", "")
            .replace("$", "")
            .strip()
        )

        selected_size = (
            self.select_size_and_add_to_bag()
        )

        return {
            "name": product_name,
            "price": product_price,
            "size": selected_size,
        }