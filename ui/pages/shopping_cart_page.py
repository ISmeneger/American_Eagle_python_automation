from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from ui.pages.base_page import BasePage


class ShoppingCartPage(BasePage):
    QUANTITY_OF_ITEMS = (
        By.CSS_SELECTOR,
        "h2[data-test-items-qty-msg]"
    )

    EDIT_ITEM_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-test-btn='editCommerceItem']"
    )

    UPDATE_BAG_BUTTON = (
        By.XPATH,
        "//button[text()='Update Bag']"
    )

    INCREASE_QUANTITY_BUTTON = (
        By.XPATH,
        "//button[@aria-label='increase']"
    )

    PRODUCT_NAME = (
        By.CSS_SELECTOR,
        "h3.cart-item-name"
    )

    PRODUCT_SIZE = (
        By.CSS_SELECTOR,
        "[data-testid='size']"
    )

    REMOVE_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-test-btn='removeCommerceItem']"
    )

    EMPTY_BAG_MESSAGE = (
        By.XPATH,
        "//h2[text()='Your bag is empty. Find something you love!']"
    )

    SIGN_IN_BUTTON = (
        By.CSS_SELECTOR,
        "a[data-testid='sign-in-link']"
    )

    CART_PAGE_HEADER = (
        By.CSS_SELECTOR,
        "h1.page-header"
    )

    FREE_SHIPPING_MESSAGE = (
        By.CSS_SELECTOR,
        "span[data-test-free-shipping]"
    )

    CART_PRODUCT_PRICE = (
        By.CSS_SELECTOR,
        "span[data-test-cart-item-sale-price], "
        "span[data-test-cart-item-price]"
    )

    SUBTOTAL_VALUE = (
        By.CSS_SELECTOR,
        "[data-test-total-row] "
        "[data-testid='row-total-value']"
    )

    CART_ITEMS = (
        By.CSS_SELECTOR,
        "div.cart-item-info"
    )

    CART_ITEM_NAME = (
        By.CSS_SELECTOR,
        "h3[data-test-cart-item-name]"
    )

    CART_ITEM_SIZE = (
        By.CSS_SELECTOR,
        "[data-testid='size']"
    )

    CART_ITEM_QUANTITY = (
        By.CSS_SELECTOR,
        "[data-testid='quantity']"
    )

    CART_ITEM_REGULAR_PRICE = (
        By.CSS_SELECTOR,
        "span[data-test-cart-item-price]"
    )

    CART_ITEM_SALE_PRICE = (
        By.CSS_SELECTOR,
        "span[data-test-cart-item-sale-price]"
    )

    def get_quantity_of_items_text(self) -> str:
        return (
            self.get_text(self.QUANTITY_OF_ITEMS)
            .splitlines()[0]
            .strip()
        )

    def click_edit_item_button(self):
        edit_button = self.wait_for_clickable(
            self.EDIT_ITEM_BUTTON
        )

        ActionChains(self.driver) \
            .scroll_to_element(edit_button) \
            .perform()

        self.wait_for_clickable(
            self.EDIT_ITEM_BUTTON
        ).click()

    def move_to_update_bag_button(self):
        update_button = self.wait_for_visible(
            self.UPDATE_BAG_BUTTON
        )

        ActionChains(self.driver) \
            .scroll_to_element(update_button) \
            .move_to_element(update_button) \
            .perform()

    def increase_product_quantity(self):
        self.click(
            self.INCREASE_QUANTITY_BUTTON
        )

    def update_bag(self):
        self.click(
            self.UPDATE_BAG_BUTTON
        )

    def get_product_name(self) -> str:
        return self.get_text(
            self.PRODUCT_NAME
        )

    def get_product_size(self) -> str:
        size_text = self.get_text(
            self.PRODUCT_SIZE
        )

        return (
            size_text
            .replace("Size:", "")
            .strip()
        )

    def remove_product_from_bag(self):
        remove_button = self.wait_for_visible(
            self.REMOVE_BUTTON
        )

        ActionChains(self.driver) \
            .scroll_to_element(remove_button) \
            .perform()

        self.wait_for_clickable(
            self.REMOVE_BUTTON
        ).click()

    def get_empty_bag_message(self) -> str:
        return self.get_text(
            self.EMPTY_BAG_MESSAGE
        )

    def click_sign_in_button(self):
        self.click(
            self.SIGN_IN_BUTTON
        )

    def get_cart_page_header(self) -> str:
        return self.get_text(
            self.CART_PAGE_HEADER
        )

    def is_free_shipping_message_displayed(self) -> bool:
        return self.is_visible(
            self.FREE_SHIPPING_MESSAGE
        )

    def get_product_price_in_cart(self) -> str:
        return self.get_text(
            self.CART_PRODUCT_PRICE
        )

    def get_subtotal_text(self) -> str:
        return (
            self.get_text(
                self.SUBTOTAL_VALUE
            )
            .strip()
        )

    def wait_for_subtotal(self, expected_subtotal: str) -> str:
        self.wait.until(
            lambda driver:
            self.wait_for_visible(
                self.SUBTOTAL_VALUE
            ).text.strip() == expected_subtotal
        )

        return self.get_text(
            self.SUBTOTAL_VALUE
        ).strip()

    def is_increase_quantity_button_enabled(self) -> bool:
        button = self.wait_for_visible(
            self.INCREASE_QUANTITY_BUTTON
        )

        return button.is_enabled()

    def increase_quantity_until_disabled(self) -> int:
        quantity = 1

        while self.is_increase_quantity_button_enabled():
            self.increase_product_quantity()
            quantity += 1

        return quantity

    def get_cart_items(self) -> list[dict]:
        self.wait.until(
            lambda driver:
            len(
                driver.find_elements(
                    *self.CART_ITEMS
                )
            ) >= 2
        )

        cart_item_elements = self.driver.find_elements(
            *self.CART_ITEMS
        )

        cart_items = []

        for item in cart_item_elements:
            name = (
                item.find_element(
                    *self.CART_ITEM_NAME
                )
                .text
                .strip()
            )

            size = (
                item.find_element(
                    *self.CART_ITEM_SIZE
                )
                .text
                .replace("Size:", "")
                .strip()
            )

            quantity = (
                item.find_element(
                    *self.CART_ITEM_QUANTITY
                )
                .text
                .replace("Qty:", "")
                .strip()
            )

            sale_prices = item.find_elements(
                *self.CART_ITEM_SALE_PRICE
            )

            if sale_prices:
                price_text = sale_prices[0].text
            else:
                price_text = (
                    item.find_element(
                        *self.CART_ITEM_REGULAR_PRICE
                    )
                    .text
                )

            price = Decimal(
                price_text
                .replace("$", "")
                .strip()
            )

            cart_items.append(
                {
                    "name": name,
                    "size": size,
                    "quantity": int(quantity),
                    "price": price,
                }
            )

        return cart_items

