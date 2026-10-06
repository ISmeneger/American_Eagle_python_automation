from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page import BasePage


class SearchResultsPage(BasePage):

    SEARCH_RESULTS_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-testid='search-results']"
    )

    PRODUCT_IMAGES = (
        By.CSS_SELECTOR,
        "img[data-test='product-image']"
    )

    NO_SEARCH_RESULTS_MESSAGE = (
        By.XPATH,
        "//h1[contains(normalize-space(.), "
        "\"Sorry! We couldn't find a match for\")]"
    )

    def get_search_results_message(self) -> str:
        return self.wait_for_visible(
            self.SEARCH_RESULTS_MESSAGE
        ).text

    def get_displayed_products_count(self) -> int:
        product_images = self.wait.until(
            EC.visibility_of_all_elements_located(
                self.PRODUCT_IMAGES
            )
        )

        return len(product_images)

    def get_no_search_results_message(self) -> str:
        return self.wait_for_visible(
            self.NO_SEARCH_RESULTS_MESSAGE
        ).text