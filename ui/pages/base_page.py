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
    POPUP_SHADOW_HOST = (By.CSS_SELECTOR, "div.bloomreach-weblayer")

    # Two distinct Bloomreach campaigns use different close-button classes.
    POPUP_EMAIL_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        'button.close-button[aria-label="Close"]',
    )
    POPUP_PROMO_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        'button.close[aria-label="Close"]',
    )
    # Keep the legacy name for any existing Page Objects referring to it.
    POPUP_CLOSE_BUTTON = POPUP_EMAIL_CLOSE_BUTTON

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

    def wait_for_present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def get_text(self, locator) -> str:
        return self.wait_for_visible(locator).text

    def is_visible(self, locator) -> bool:
        return self.wait_for_visible(locator).is_displayed()

    def accept_cookies_if_available(self) -> bool:
        """Dismiss a visible cookie banner without waiting when it is absent."""
        for button in self.driver.find_elements(*self.COOKIE_BUTTON):
            try:
                if button.is_displayed() and button.is_enabled():
                    button.click()
                    return True
            except (StaleElementReferenceException, ElementClickInterceptedException):
                continue
        return False

    def _has_visible_bloomreach(self) -> bool:
        try:
            return any(
                host.is_displayed()
                for host in self.driver.find_elements(*self.POPUP_SHADOW_HOST)
            )
        except StaleElementReferenceException:
            return True

    def close_popup_if_present(self) -> bool:
        """Close visible email/promo Bloomreach layers, including open Shadow DOM."""
        return bool(self.driver.execute_script(
            """
            const selectors = [
                'button.close-button[aria-label="Close"]',
                'button.close[aria-label="Close"]'
            ];
            let closed = false;
            for (const host of document.querySelectorAll('div.bloomreach-weblayer')) {
                if (!host.getClientRects().length) continue;
                const root = host.shadowRoot || host;
                for (const selector of selectors) {
                    const button = root.querySelector(selector);
                    if (button) {
                        button.click();
                        closed = true;
                        break;
                    }
                }
            }
            return closed;
            """
        ))

    def close_location_popup_if_present(self) -> bool:
        """Dismiss the shipping-location dialog if its close button is visible."""
        for button in self.driver.find_elements(*self.LOCATION_POPUP_CLOSE_BUTTON):
            try:
                if not button.is_displayed():
                    continue
                self.driver.execute_script("arguments[0].click();", button)
                WebDriverWait(self.driver, 3).until(
                    EC.invisibility_of_element_located(
                        self.LOCATION_POPUP_CLOSE_BUTTON
                    )
                )
                return True
            except (
                ElementClickInterceptedException,
                NoSuchElementException,
                StaleElementReferenceException,
                TimeoutException,
            ):
                continue
        return False

    def close_popup_if_available(self):
        """Handle location and delayed Bloomreach offers (existing API)."""
        self.close_location_popup_if_present()
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: self.close_popup_if_present()
            )
            self.wait.until(lambda driver: not self._has_visible_bloomreach())
        except TimeoutException:
            pass

    def close_blocking_overlays_if_available(self):
        self.accept_cookies_if_available()
        self.close_popup_if_available()
        # A banner may appear while Bloomreach is being dismissed.
        self.accept_cookies_if_available()

    def safe_click(self, locator, max_attempts: int = 3):
        """Retry a regular Selenium click after late overlays or stale DOM changes."""
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        for attempt in range(max_attempts):
            try:
                self.wait_for_clickable(locator).click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException):
                if attempt == max_attempts - 1:
                    raise
                self.close_blocking_overlays_if_available()
                self.wait.until(lambda driver: not self._has_visible_bloomreach())

    def click(self, locator):
        self.safe_click(locator)

    def click_nearest_interactive(self, locator, max_attempts: int = 3):
        """Click the nearest button/link of a located icon or nested element."""
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        for attempt in range(max_attempts):
            try:
                element = self.wait_for_visible(locator)
                parent = self.driver.execute_script(
                    "return arguments[0].closest('button, a, [role=\"button\"]');",
                    element,
                )
                if parent is None:
                    raise AssertionError(
                        f"Clickable parent was not found for locator: {locator}"
                    )
                self.wait.until(lambda driver: parent.is_displayed() and parent.is_enabled())
                parent.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException):
                if attempt == max_attempts - 1:
                    raise
                self.close_blocking_overlays_if_available()
                self.wait.until(lambda driver: not self._has_visible_bloomreach())
