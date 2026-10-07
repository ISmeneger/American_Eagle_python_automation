from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class HeaderComponent(BasePage):

    LOGO = (
        By.XPATH,
        "//a[@title='Shop AE']"
    )

    FEATURED_OFFERS = (
        By.XPATH,
        "//li[@data-test='top-link-wrapper']//button[contains(@class, 'link_EZ5lj')]"
    )

    NEW = (
        By.CSS_SELECTOR,
        "button[aria-label='New']"
    )

    WOMEN = (
        By.XPATH,
        "//a[text()='Women']"
    )

    MEN = (
        By.XPATH,
        "//a[text()='Men']"
    )

    JEANS = (
        By.CSS_SELECTOR,
        "a[href*='/x/jeans']"
    )

    AERIE = (
        By.CSS_SELECTOR,
        "li[data-test='top-link-wrapper'] > a[href*='/c/aerie/']"
    )

    CLEARANCE = (
        By.XPATH,
        "//a[contains(@href, '/x/clearance')]"
    )

    SEARCH_BUTTON = (
        By.NAME,
        "search-cta"
    )

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[name='search']"
    )

    ACCOUNT_ICON = (
        By.CSS_SELECTOR,
        "svg[data-testid='icon-account']"
    )

    SIGN_IN_BUTTON = (
        By.CSS_SELECTOR,
        "a[data-testid='sign-in-link']"
    )

    ACCOUNT_MODAL_TITLE = (
        By.CSS_SELECTOR,
        "h2.wc-side-tray__title"
    )

    CREATE_ACCOUNT_BUTTON = (
        By.CSS_SELECTOR,
        "a[data-testid='register-link']"
    )

    FAVORITES_ICON = (
        By.CSS_SELECTOR,
        "svg[data-testid='icon-favorites']"
    )

    FAVORITES_TITLE = (
        By.XPATH,
        "//h1[text()='Favorites']"
    )

    BAG_BUTTON = (
        By.CSS_SELECTOR,
        "a.qa-tnav-bag-icon"
    )

    BAG_TITLE = (
        By.XPATH,
        "//h1[text()='Shopping Bag']"
    )

    def is_logo_visible(self) -> bool:
        return self.is_visible(self.LOGO)

    def is_featured_offers_visible(self) -> bool:
        return self.is_visible(self.FEATURED_OFFERS)

    def is_new_visible(self) -> bool:
        return self.is_visible(self.NEW)

    def is_women_visible(self) -> bool:
        return self.is_visible(self.WOMEN)

    def is_men_visible(self) -> bool:
        return self.is_visible(self.MEN)

    def is_jeans_visible(self) -> bool:
        return self.is_visible(self.JEANS)

    def is_aerie_visible(self) -> bool:
        return self.is_visible(self.AERIE)

    def is_clearance_visible(self) -> bool:
        return self.is_visible(self.CLEARANCE)

    def is_search_button_visible(self) -> bool:
        return self.is_visible(self.SEARCH_BUTTON)

    def click_search_button(self):
        self.click(self.SEARCH_BUTTON)

    def is_search_input_visible(self) -> bool:
        return self.is_visible(self.SEARCH_INPUT)

    def is_account_icon_visible(self) -> bool:
        return self.is_visible(self.ACCOUNT_ICON)

    def is_favorites_button_visible(self) -> bool:
        return self.is_visible(self.FAVORITES_BUTTON)

    def is_bag_button_visible(self) -> bool:
        return self.is_visible(self.BAG_BUTTON)

    def enter_search_query(self, query: str):
        search_input = self.wait_for_visible(self.SEARCH_INPUT)

        search_input.click()
        search_input.send_keys(query)

        self.wait.until(
            lambda driver: (
                    (search_input.get_property("value") or "")
                    .strip()
                    .lower()
                    == query.lower()
            )
        )

    def select_search_suggestion(self, query: str):
        suggestion_locator = (
            By.CSS_SELECTOR,
            f"button[name='select-suggestion']"
            f"[aria-label='search for {query} instead']"
        )

        self.wait_for_clickable(
            suggestion_locator
        ).click()

    def submit_search_query(self):
        search_input = self.wait_for_visible(
            self.SEARCH_INPUT
        )

        search_input.send_keys(Keys.ENTER)

    def click_account_button(self):
        self.click_nearest_interactive(self.ACCOUNT_ICON)

    def get_account_title_text(self) -> str:
        return self.get_text(self.ACCOUNT_MODAL_TITLE)

    def is_sign_in_button_visible(self) -> bool:
        return self.is_visible(self.SIGN_IN_BUTTON)

    def is_create_account_button_visible(self) -> bool:
        return self.is_visible(self.CREATE_ACCOUNT_BUTTON)

    def click_favorites_button(self):
        self.click_nearest_interactive(self.FAVORITES_ICON)

    def get_favorites_title_text(self) -> str:
        return self.get_text(self.FAVORITES_TITLE)

    def click_bag_button(self):
        self.click(self.BAG_BUTTON)

    def get_bag_title_text(self) -> str:
        return self.get_text(self.BAG_TITLE)

    def click_sign_in_button(self):
        self.click(self.SIGN_IN_BUTTON)

    def click_create_account_button(self):
        self.click(self.CREATE_ACCOUNT_BUTTON)