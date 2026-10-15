from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
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
        "button[aria-label='dismiss cookie message']",
    )
    POPUP_SHADOW_HOST = (
        By.CSS_SELECTOR,
        "div.bloomreach-weblayer",
    )
    POPUP_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        'button.close-button[aria-label="Close"]',
    )
    LOCATION_POPUP_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        'button[data-test-btn="close"][aria-label="Close"]',
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
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        element = self.wait_for_clickable(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.close_blocking_overlays_if_available()
            self.wait.until(lambda driver: not self._has_visible_bloomreach())
            self.wait_for_clickable(locator).click()

    def get_text(self, locator) -> str:
        return self.wait_for_visible(locator).text

    def is_visible(self, locator) -> bool:
        return self.wait_for_visible(locator).is_displayed()

    def accept_cookies_if_available(self):
        # No two-second wait when the cookie banner isn't on the page.
        for button in self.driver.find_elements(*self.COOKIE_BUTTON):
            try:
                if button.is_displayed() and button.is_enabled():
                    button.click()
                    return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                continue

    def _has_visible_bloomreach(self) -> bool:
        try:
            return any(
                host.is_displayed()
                for host in self.driver.find_elements(*self.POPUP_SHADOW_HOST)
            )
        except StaleElementReferenceException:
            return True

    def close_popup_if_present(self) -> bool:
        # Preserve the working JS approach for Bloomreach's open Shadow DOM.
        return bool(self.driver.execute_script("""
            const hosts = document.querySelectorAll('div.bloomreach-weblayer');
            for (const host of hosts) {
                const root = host.shadowRoot || host;
                const button = root.querySelector(
                    'button.close-button[aria-label="Close"]'
                );
                if (button) {
                    button.click();
                    return true;
                }
            }
            return false;
        """))

    def close_popup_if_available(self):
        self.close_location_popup_if_present()

        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: self.close_popup_if_present()
            )
        except TimeoutException:
            pass

    def close_blocking_overlays_if_available(self):
        self.accept_cookies_if_available()
        self.close_popup_if_available()

    def click_nearest_interactive(self, locator):
        element = self.wait_for_visible(locator)
        clickable_parent = self.driver.execute_script("""
            return arguments[0].closest('button, a, [role="button"]');
        """, element)
        if clickable_parent is None:
            raise AssertionError(
                f"Clickable parent was not found for locator: {locator}"
            )
        self.wait.until(
            lambda driver: clickable_parent.is_displayed()
            and clickable_parent.is_enabled()
        )
        try:
            clickable_parent.click()
        except ElementClickInterceptedException:
            self.close_blocking_overlays_if_available()
            element = self.wait_for_visible(locator)
            clickable_parent = self.driver.execute_script("""
                return arguments[0].closest('button, a, [role="button"]');
            """, element)
            clickable_parent.click()

    def wait_for_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def close_location_popup_if_present(self):
        close_buttons = self.driver.find_elements(
            *self.LOCATION_POPUP_CLOSE_BUTTON
        )

        for button in close_buttons:
            try:
                if not button.is_displayed():
                    continue

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                WebDriverWait(self.driver, 3).until(
                    EC.invisibility_of_element_located(
                        self.LOCATION_POPUP_CLOSE_BUTTON
                    )
                )

                return

            except (
                    ElementClickInterceptedException,
                    NoSuchElementException,
                    StaleElementReferenceException,
                    TimeoutException,
            ):
                continue
