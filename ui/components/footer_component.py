from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class FooterComponent(BasePage):

    COPYRIGHT_TEXT = (
        By.CSS_SELECTOR,
        "p[class*='copyright']"
    )

    FOOTER_IMAGE = (
        By.CSS_SELECTOR,
        "img[src*='Footer-logos.svg']"
    )

    def scroll_to_copyright_text(self):
        element = self.wait_for_visible(
            self.COPYRIGHT_TEXT
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )

        self.wait_for_visible(
            self.COPYRIGHT_TEXT
        )

    def get_copyright_text(self) -> str:
        return self.get_text(
            self.COPYRIGHT_TEXT
        )

    def scroll_to_footer_image(self):
        element = self.wait_for_visible(
            self.FOOTER_IMAGE
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )

        self.wait_for_visible(
            self.FOOTER_IMAGE
        )

    def is_footer_image_visible(self) -> bool:
        return self.is_visible(
            self.FOOTER_IMAGE
        )