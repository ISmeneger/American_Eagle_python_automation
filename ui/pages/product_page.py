from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ui.pages.base_page import BasePage
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)


class ProductPage(BasePage):
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

    PRODUCT_PRICE = (
        By.CSS_SELECTOR,
        "div.product-sale-price, div[data-testid='list-price']"
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

    INCREASE_QUANTITY_BUTTON = (
        By.XPATH,
        "//button[@aria-label='increase']"
    )

    def select_first_available_size(self):
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                # Закрываем popup, если он уже успел появиться
                self.close_popup_if_present()

                size_dropdown = self.wait_for_clickable(
                    self.SIZE_DROPDOWN
                )

                ActionChains(self.driver) \
                    .scroll_to_element(size_dropdown) \
                    .perform()

                # Открываем dropdown только если он ещё закрыт
                if (
                        size_dropdown.get_attribute("aria-expanded")
                        != "true"
                ):
                    size_dropdown.click()

                # Получаем элемент заново через locator,
                # чтобы не работать со старым WebElement
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

                first_available_size = available_sizes[0]

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
                    ).text.strip() == expected_size
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

    def get_selected_size(self) -> str:
        return (
            self.wait_for_visible(
                self.SELECTED_SIZE_TEXT
            )
            .text
            .strip()
        )

    def get_product_price(self) -> str:
        return self.get_text(
            self.PRODUCT_PRICE
        )

    def click_add_to_bag_button(self):
        self.click(
            self.ADD_TO_BAG_BUTTON
        )

        self.wait_for_visible(
            self.ADDED_TO_BAG_MESSAGE
        )

        self.wait_for_clickable(
            self.VIEW_BAG_BUTTON
        )

    def get_added_to_bag_message(self) -> str:
        return self.get_text(
            self.ADDED_TO_BAG_MESSAGE
        )

    def open_shopping_bag(self):
        self.click(
            self.VIEW_BAG_BUTTON
        )

        navigation_wait = WebDriverWait(
            self.driver,
            30,
        )

        navigation_wait.until(
            EC.url_contains("/cart")
        )

    def is_increase_quantity_button_enabled(self) -> bool:
        return self.wait_for_visible(
            self.INCREASE_QUANTITY_BUTTON
        ).is_enabled()

    def increase_quantity(self):
        self.click(
            self.INCREASE_QUANTITY_BUTTON
        )

    def increase_quantity_until_disabled(self) -> int:
        quantity = 1

        while self.is_increase_quantity_button_enabled():
            self.increase_quantity()
            quantity += 1

        return quantity