from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from ui.pages.base_page import BasePage
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)


class JeansPage(BasePage):
    JEANS_MENU = (
        By.CSS_SELECTOR,
        "a[href='/us/en/x/jeans?menu=cat4840004&pagetype=slp']"
    )

    MEN_JEANS_VIEW_ALL = (
        By.XPATH,
        "//a[@href='/us/en/c/men/bottoms/jeans/cat6430041' "
        "and normalize-space()='View All']"
    )

    FIRST_PRODUCT = (
        By.XPATH,
        "(//*[@data-test-product-list]"
        "//img[@data-test='product-image'])[1]"
    )

    def move_to_jeans_menu(self):
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                self.close_popup_if_present()

                jeans_menu = self.wait_for_visible(
                    self.JEANS_MENU
                )

                ActionChains(self.driver) \
                    .scroll_to_element(jeans_menu) \
                    .move_to_element(jeans_menu) \
                    .perform()

                self.wait_for_visible(
                    self.MEN_JEANS_VIEW_ALL
                )

                return

            except (
                    StaleElementReferenceException,
                    TimeoutException,
            ):
                self.close_popup_if_available()

                if attempt == max_attempts - 1:
                    raise

    def click_mens_view_all(self):
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                self.close_popup_if_present()

                view_all = self.wait_for_clickable(
                    self.MEN_JEANS_VIEW_ALL
                )

                ActionChains(self.driver) \
                    .scroll_to_element(view_all) \
                    .move_to_element(view_all) \
                    .perform()

                view_all.click()

                return

            except (
                    ElementNotInteractableException,
                    StaleElementReferenceException,
                    TimeoutException,
            ):
                self.move_to_jeans_menu()

                if attempt == max_attempts - 1:
                    raise

    def open_first_available_product(self) -> str:
        first_product = self.wait_for_clickable(
            self.FIRST_PRODUCT
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