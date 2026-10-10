from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ui.components.header_component import HeaderComponent
from ui.pages.base_page import BasePage


class ProductPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)

    SIZE_DROPDOWN = (
        By.CSS_SELECTOR,
        "div[data-test-dropdown-toggle]"
    )

    AVAILABLE_SIZES = (
        By.CSS_SELECTOR,
        "ul.dropdown-menu li:not(.visually-disabled) "
        "a[role='menuitem']"
    )

    SELECTED_SIZE_TEXT = (
        By.CSS_SELECTOR,
        "div[data-test-dropdown-toggle] span[data-test-text]"
    )

    SALE_PRICE = (
        By.CSS_SELECTOR,
        "[data-testid='sale-price']"
    )

    LIST_PRICE = (
        By.CSS_SELECTOR,
        "[data-testid='list-price']"
    )

    ADD_TO_BAG_BUTTON = (
        By.NAME,
        "addToBag"
    )

    ADDED_TO_BAG_MESSAGE = (
        By.XPATH,
        "//h2[text()='Added to bag!']"
    )

    VIEW_BAG_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-test-btn='viewBag']"
    )

    def select_first_available_size(self):
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                self.close_popup_if_present()

                size_dropdown = self.wait_for_clickable(
                    self.SIZE_DROPDOWN
                )

                ActionChains(self.driver) \
                    .scroll_to_element(size_dropdown) \
                    .perform()

                if (
                    size_dropdown.get_attribute(
                        "aria-expanded"
                    )
                    != "true"
                ):
                    size_dropdown.click()

                self.wait.until(
                    lambda driver:
                    driver.find_element(
                        *self.SIZE_DROPDOWN
                    ).get_attribute(
                        "aria-expanded"
                    ) == "true"
                )

                available_sizes = self.wait.until(
                    EC.visibility_of_all_elements_located(
                        self.AVAILABLE_SIZES
                    )
                )

                if not available_sizes:
                    raise AssertionError(
                        "No available sizes found"
                    )

                first_available_size = (
                    available_sizes[0]
                )

                expected_size = (
                    first_available_size
                    .find_element(
                        By.CSS_SELECTOR,
                        "span.sku-size"
                    )
                    .text
                    .strip()
                )

                first_available_size.click()

                self.wait.until(
                    lambda driver:
                    driver.find_element(
                        *self.SELECTED_SIZE_TEXT
                    ).text.strip()
                    == expected_size
                )

                return

            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
                TimeoutException,
            ):
                self.close_popup_if_available()

                if attempt == max_attempts - 1:
                    raise

        raise AssertionError(
            "Failed to select product size"
        )

    def get_selected_size(self) -> str:
        return (
            self.get_text(
                self.SELECTED_SIZE_TEXT
            )
            .strip()
        )

    def get_product_price(self) -> str:
        sale_prices = self.driver.find_elements(
            *self.SALE_PRICE
        )

        for sale_price in sale_prices:
            if sale_price.is_displayed():
                price_text = sale_price.text.strip()

                if price_text:
                    return price_text

        return (
            self.wait_for_visible(
                self.LIST_PRICE
            )
            .text
            .strip()
        )

    def click_add_to_bag_button(self):
        self.click(
            self.ADD_TO_BAG_BUTTON
        )

    def get_added_to_bag_message(self) -> str:
        return (
            self.get_text(
                self.ADDED_TO_BAG_MESSAGE
            )
            .strip()
        )

    def open_shopping_bag(self):
        try:
            self.click(
                self.VIEW_BAG_BUTTON
            )

        except (
                TimeoutException,
                ElementClickInterceptedException,
        ):
            self.header.click_bag_button()

        WebDriverWait(
            self.driver,
            30
        ).until(
            EC.url_contains("/cart")
        )