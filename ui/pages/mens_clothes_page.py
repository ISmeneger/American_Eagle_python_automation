from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)

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

    SORT_BY_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-test-accordion='Sort By']"
    )

    PRICE_LOW_TO_HIGH = (
        By.XPATH,
        "//label[normalize-space()='Price: Low to High']"
    )

    PRODUCT_CARDS = (
        By.CSS_SELECTOR,
        "[data-test-details]"
    )

    SALE_PRICE = (
        By.CSS_SELECTOR,
        "[data-testid='sale-price']"
    )

    LIST_PRICE = (
        By.CSS_SELECTOR,
        "[data-testid='list-price']"
    )

    PRICE_FILTER_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-test-accordion='Price']"
    )

    PRICE_25_TO_50_CHECKBOX = (
        By.CSS_SELECTOR,
        "[data-test-checkbox='$25 - $50'] input[type='checkbox']"
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

    def select_price_low_to_high(self):
        sort_button = self.wait_for_clickable(
            self.SORT_BY_BUTTON
        )

        if (
                sort_button.get_attribute("aria-expanded")
                != "true"
        ):
            sort_button.click()

        self.click(self.PRICE_LOW_TO_HIGH)

    def get_product_prices(self) -> list[Decimal]:
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                product_cards = self.wait.until(
                    EC.visibility_of_all_elements_located(
                        self.PRODUCT_CARDS
                    )
                )

                prices = []

                for product_card in product_cards:
                    sale_prices = product_card.find_elements(
                        *self.SALE_PRICE
                    )

                    if sale_prices:
                        price_text = (
                            sale_prices[0]
                            .text
                            .strip()
                        )
                    else:
                        list_prices = product_card.find_elements(
                            *self.LIST_PRICE
                        )

                        if not list_prices:
                            continue

                        price_text = (
                            list_prices[0]
                            .text
                            .strip()
                        )

                    price = Decimal(
                        price_text
                        .replace("$", "")
                        .replace(",", "")
                        .strip()
                    )

                    prices.append(price)

                if prices:
                    return prices

            except StaleElementReferenceException:
                if attempt == max_attempts - 1:
                    raise

        raise AssertionError(
            "Product prices were not found"
        )

    def select_price_filter_25_to_50(self):
        price_filter_button = self.wait_for_clickable(
            self.PRICE_FILTER_BUTTON
        )

        if (
                price_filter_button.get_attribute("aria-expanded")
                != "true"
        ):
            price_filter_button.click()

        checkbox = self.wait_for_present(
            self.PRICE_25_TO_50_CHECKBOX
        )

        if not checkbox.is_selected():
            self.driver.execute_script(
                "arguments[0].click();",
                checkbox,
            )