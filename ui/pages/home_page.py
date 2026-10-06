from selenium.webdriver.remote.webdriver import WebDriver

from ui.components.footer_component import FooterComponent
from ui.components.header_component import HeaderComponent
from ui.config import BASE_URL
from ui.pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.footer = FooterComponent(driver)

    def open(self, close_overlays: bool = True):
        self.open_url(BASE_URL)

        if close_overlays:
            self.close_blocking_overlays_if_available()

    def is_opened(self) -> bool:
        return "American Eagle" in self.get_title()