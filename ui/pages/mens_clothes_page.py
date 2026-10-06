from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page import BasePage


class MensClothesPage(BasePage):
    MEN_MENU = (
        By.XPATH,
        "//a[text()='Men']"
    )

    VIEW_ALL_CATEGORIES = (
        By.XPATH,
        "//a[contains(@href, '/men/mens') and text()='View All']"
    )

    MENS_CLOTHES_TITLE = (
        By.CSS_SELECTOR,
        "[data-testid='page-title'] h1"
    )

    PRODUCT_ITEMS = (
        By.CSS_SELECTOR,
        "img[data-test='product-image']"
    )

    def move_to_men_menu(self):
        men_menu = self.wait_for_visible(
            self.MEN_MENU
        )

        ActionChains(self.driver) \
            .scroll_to_element(men_menu) \
            .move_to_element(men_menu) \
            .perform()

        self.wait_for_visible(
            self.VIEW_ALL_CATEGORIES
        )

    def click_view_all_categories(self):
        view_all = self.wait_for_clickable(
            self.VIEW_ALL_CATEGORIES
        )

        ActionChains(self.driver) \
            .move_to_element(view_all) \
            .perform()

        view_all.click()

    def get_mens_page_title(self) -> str:
        return self.get_text(
            self.MENS_CLOTHES_TITLE
        )

    def open_first_available_product(self) -> str:
        try:
            products = self.wait.until(
                EC.visibility_of_all_elements_located(
                    self.PRODUCT_ITEMS
                )
            )
        except TimeoutException:
            self.close_popup_if_available()

            products = self.wait.until(
                EC.visibility_of_all_elements_located(
                    self.PRODUCT_ITEMS
                )
            )

        if not products:
            raise AssertionError(
                "No products found in Men's catalog"
            )

        first_product = self.wait.until(
            EC.element_to_be_clickable(
                products[0]
            )
        )

        product_name = (
                first_product.get_attribute("alt")
                or ""
        ).strip()

        if not product_name:
            raise AssertionError(
                "Product name was not found"
            )

        first_product.click()

        return product_name