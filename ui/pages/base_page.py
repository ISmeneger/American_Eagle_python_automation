from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    NoSuchShadowRootException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:

    COOKIE_BUTTON = (
        By.CSS_SELECTOR,
        "button[aria-label='dismiss cookie message']"
    )

    POPUP_SHADOW_HOST = (
        By.CSS_SELECTOR,
        "div.bloomreach-weblayer"
    )

    POPUP_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "button.close-button[aria-label='Close'], "
        "button.close[aria-label='Close']"
    )

    LOCATION_POPUP_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        'button[data-test-btn="close"][aria-label="Close"]'
    )

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, url: str):
        self.driver.get(url)

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

    def wait_for_visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator):
        element = self.wait_for_clickable(locator)

        try:
            element.click()

        except ElementClickInterceptedException:
            self.close_popup_if_available()

            self.wait.until(
                lambda driver:
                not any(
                    popup.is_displayed()
                    for popup in driver.find_elements(
                        *self.POPUP_SHADOW_HOST
                    )
                )
            )

            self.wait_for_clickable(locator).click()

    def get_text(self, locator) -> str:
        return self.wait_for_visible(locator).text

    def is_visible(self, locator) -> bool:
        return self.wait_for_visible(locator).is_displayed()

    def accept_cookies_if_available(self):
        try:
            cookie_wait = WebDriverWait(self.driver, 2)

            cookie_wait.until(
                EC.element_to_be_clickable(self.COOKIE_BUTTON)
            ).click()

        except (
            TimeoutException,
            NoSuchElementException,
            StaleElementReferenceException,
        ):
            pass

    def close_popup_if_available(self):
        self.close_location_popup_if_present()
        popup_wait = WebDriverWait(self.driver, 2)

        try:
            popup_wait.until(self._try_close_popup)

        except TimeoutException:
            pass

    def close_popup_if_present(self) -> bool:
        try:
            shadow_hosts = self.driver.find_elements(
                *self.POPUP_SHADOW_HOST
            )

            for shadow_host in shadow_hosts:
                if not shadow_host.is_displayed():
                    continue

                shadow_root = shadow_host.shadow_root

                close_buttons = shadow_root.find_elements(
                    *self.POPUP_CLOSE_BUTTON
                )

                if not close_buttons:
                    continue

                close_button = close_buttons[0]

                if (
                        close_button.is_displayed()
                        and close_button.is_enabled()
                ):
                    self.driver.execute_script(
                        "arguments[0].click();",
                        close_button,
                    )
                    return True

        except (
                NoSuchElementException,
                NoSuchShadowRootException,
                StaleElementReferenceException,
                ElementClickInterceptedException,
        ):
            pass

        return False

    def _try_close_popup(self, driver):
        try:
            shadow_host = driver.find_element(
                *self.POPUP_SHADOW_HOST
            )

            shadow_root = shadow_host.shadow_root

            close_button = shadow_root.find_element(
                *self.POPUP_CLOSE_BUTTON
            )

            if close_button.is_displayed() and close_button.is_enabled():
                close_button.click()
                return True

        except (
            NoSuchElementException,
            NoSuchShadowRootException,
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ):
            return False

        return False

    def close_blocking_overlays_if_available(self):
        self.accept_cookies_if_available()
        self.close_popup_if_available()

    def click_nearest_interactive(self, locator):
        element = self.wait_for_visible(locator)

        clickable_parent = self.driver.execute_script(
            """
            return arguments[0].closest(
                'button, a, [role="button"]'
            );
            """,
            element,
        )

        if clickable_parent is None:
            raise AssertionError(
                f"Clickable parent was not found for locator: {locator}"
            )

        self.wait.until(
            lambda driver:
            clickable_parent.is_displayed()
            and clickable_parent.is_enabled()
        )

        clickable_parent.click()

    def wait_for_present(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def close_location_popup_if_present(self):
        try:
            close_button = WebDriverWait(
                self.driver,
                3
            ).until(
                EC.element_to_be_clickable(
                    self.LOCATION_POPUP_CLOSE_BUTTON
                )
            )

            try:
                close_button.click()
            except (
                    ElementClickInterceptedException,
                    StaleElementReferenceException,
            ):
                close_button = self.driver.find_element(
                    *self.LOCATION_POPUP_CLOSE_BUTTON
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    close_button,
                )

            WebDriverWait(
                self.driver,
                3
            ).until(
                EC.invisibility_of_element_located(
                    self.LOCATION_POPUP_CLOSE_BUTTON
                )
            )

        except (
                TimeoutException,
                NoSuchElementException,
                StaleElementReferenceException,
        ):
            pass