import allure
import pytest

from ui.pages.home_page import HomePage
from ui.pages.search_results_page import SearchResultsPage


pytestmark = [
    pytest.mark.ui,
    pytest.mark.home_page,
]


@pytest.mark.smoke
@pytest.mark.positive
@allure.feature("Home Page")
@allure.story("Search")
@allure.title("Display search input after clicking search button")
def test_search_input_is_visible_after_click(driver):
    home_page = HomePage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Click search button"):
        home_page.header.click_search_button()

    with allure.step("Verify search input is visible"):
        assert home_page.header.is_search_input_visible()


@pytest.mark.positive
@allure.feature("Home Page")
@allure.story("Search")
@allure.title("Search existing products")
def test_search_existing_products(driver):
    home_page = HomePage(driver)
    search_results_page = SearchResultsPage(driver)

    query = "jeans"

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step(f"Search for product: {query}"):
        home_page.header.click_search_button()
        home_page.header.enter_search_query(query)
        home_page.header.submit_search_query()

    with allure.step("Verify search results are displayed"):
        assert search_results_page.get_displayed_products_count() > 0


@pytest.mark.negative
@pytest.mark.defect
@pytest.mark.xfail(
    reason="Known defect: search returns products for non-existing queries",
    strict=False,
)
@allure.feature("Home Page")
@allure.story("Search")
@allure.title("Search non-existing product")
def test_search_non_existing_product(driver):
    home_page = HomePage(driver)
    search_results_page = SearchResultsPage(driver)

    query = "zzqxy987654321nonexistentproduct"

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step(f"Search for non-existing product: {query}"):
        home_page.header.click_search_button()
        home_page.header.enter_search_query(query)
        home_page.header.submit_search_query()

    with allure.step("Verify no search results message is displayed"):
        message = search_results_page.get_no_search_results_message()

        assert "Sorry! We couldn't find a match for" in message