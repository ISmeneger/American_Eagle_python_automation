from decimal import Decimal

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

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

    FREE_SHIPPING_MESSAGE = (
        By.CSS_SELECTOR,
        "span[data-test-free-shipping]"
    )

    CART_SALE_PRICE = (
        By.CSS_SELECTOR,
        "span[data-test-cart-item-sale-price]"
    )

    CART_REGULAR_PRICE = (
        By.CSS_SELECTOR,
        "span[data-test-cart-item-price]"
    )

    SUBTOTAL_VALUE = (
        By.CSS_SELECTOR,
        "[data-test-total-row] "
        "[data-testid='row-total-value']"
    )

    SHIPPING_VALUE = (
        By.CSS_SELECTOR,
        "[data-testid='row-shipping'] "
        "[data-testid='row-shipping-value']"
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

    CART_ITEM_NAME_LINK = (
        By.CSS_SELECTOR,
        "h3[data-test-cart-item-name] a"
    )

    CART_ITEM_CONTAINER = (
        By.CSS_SELECTOR,
        "div[data-testid='commerce-item']"
    )

    def get_quantity_of_items_text(self) -> str:
        return (
            self.get_text(
                self.QUANTITY_OF_ITEMS
            )
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
        return (
            self.get_text(
                self.PRODUCT_NAME
            )
            .strip()
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
        return (
            self.get_text(
                self.EMPTY_BAG_MESSAGE
            )
            .strip()
        )

    def click_sign_in_button(self):
        self.click(
            self.SIGN_IN_BUTTON
        )

    def is_free_shipping_message_displayed(
        self,
    ) -> bool:
        return self.is_visible(
            self.FREE_SHIPPING_MESSAGE
        )

    def get_product_price_in_cart(self) -> str:
        sale_prices = self.driver.find_elements(
            *self.CART_SALE_PRICE
        )

        for sale_price in sale_prices:
            if sale_price.is_displayed():
                price_text = sale_price.text.strip()

                if price_text:
                    return price_text

        return (
            self.wait_for_visible(
                self.CART_REGULAR_PRICE
            )
            .text
            .strip()
        )

    def wait_for_subtotal(
        self,
        expected_subtotal: str,
    ) -> str:
        """Wait until the checkout summary displays the expected amount."""
        def expected_value_is_visible(driver):
            for element in driver.find_elements(*self.SUBTOTAL_VALUE):
                if element.is_displayed():
                    value = element.text.strip()
                    if value == expected_subtotal:
                        return value
            return False

        return self.wait.until(
            expected_value_is_visible,
            message=f"Sub Total did not reach {expected_subtotal}",
        )

    def is_increase_quantity_button_enabled(
        self,
    ) -> bool:
        button = self.wait_for_visible(
            self.INCREASE_QUANTITY_BUTTON
        )

        return button.is_enabled()

    def increase_quantity_until_disabled(
        self,
    ) -> int:
        quantity = 1

        while (
            self.is_increase_quantity_button_enabled()
        ):
            self.increase_product_quantity()
            quantity += 1

        return quantity

    def get_cart_items(
            self,
            expected_count: int = 2,
    ) -> list[dict]:
        self.wait.until(
            lambda driver: len(
                driver.find_elements(*self.CART_ITEMS)
            ) == expected_count
        )

        cart_item_elements = (
            self.driver.find_elements(
                *self.CART_ITEMS
            )
        )

        cart_items = []

        for item in cart_item_elements:
            name = self.wait.until(
                lambda driver: (
                    item.find_element(
                        *self.CART_ITEM_NAME_LINK
                    )
                    .text
                    .strip()
                )
            )

            size = (
                item.find_element(
                    *self.CART_ITEM_SIZE
                )
                .text
                .replace("Size:", "")
                .strip()
            )

            quantity = self.wait.until(
                lambda driver: (
                    item.find_element(*self.CART_ITEM_QUANTITY)
                    .text.replace("Qty:", "").strip()
                ) or False
            )

            sale_prices = item.find_elements(
                *self.CART_ITEM_SALE_PRICE
            )

            if (
                sale_prices
                and sale_prices[0].is_displayed()
                and sale_prices[0].text.strip()
            ):
                price_text = (
                    sale_prices[0]
                    .text
                    .strip()
                )

            else:
                price_text = (
                    item.find_element(
                        *self.CART_ITEM_REGULAR_PRICE
                    )
                    .text
                    .strip()
                )

            price = Decimal(
                price_text
                .replace("$", "")
                .replace(",", "")
                .strip()
            )

            if not quantity.isdigit():
                raise AssertionError(
                    f"Invalid quantity for product '{name}': "
                    f"{quantity!r}"
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

    def remove_product_by_name(self, product_name: str):
        def find_remove_button(driver):
            cart_items = driver.find_elements(
                *self.CART_ITEM_CONTAINER
            )

            for item in cart_items:
                name_elements = item.find_elements(
                    *self.CART_ITEM_NAME_LINK
                )

                if not name_elements:
                    continue

                name = name_elements[0].text.strip()

                if name == product_name:
                    buttons = item.find_elements(
                        *self.REMOVE_BUTTON
                    )

                    if buttons:
                        return buttons[0]

            return False

        remove_button = self.wait.until(
            find_remove_button
        )

        ActionChains(self.driver) \
            .scroll_to_element(remove_button) \
            .perform()

        remove_button.click()

    def get_shipping_cost(self) -> Decimal:
        """Read the displayed shipping charge after it appears in the summary."""
        def shipping_text_is_ready(driver):
            for element in driver.find_elements(*self.SHIPPING_VALUE):
                if element.is_displayed():
                    value = element.text.strip()
                    if value:
                        return value
            return False

        shipping_text = self.wait.until(
            shipping_text_is_ready,
            message="Shipping amount did not appear in Shopping Bag",
        )

        if shipping_text.lower() in ("free", "$0", "$0.00"):
            return Decimal("0.00")

        return Decimal(
            shipping_text.replace("$", "").replace(",", "").strip()
        )
