import allure
import pytest

from ui.pages.home_page import HomePage


pytestmark = [
    pytest.mark.ui,
    pytest.mark.home_page,
]


@pytest.mark.smoke
@pytest.mark.positive
@allure.feature("Home Page")
@allure.story("Header")
@allure.title("Display main header elements")
def test_header_main_elements_are_visible(driver):
    home_page = HomePage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    header = home_page.header

    with allure.step("Verify main header elements are visible"):
        assert header.is_logo_visible()
        assert header.is_featured_offers_visible()
        assert header.is_new_visible()
        assert header.is_women_visible()
        assert header.is_men_visible()
        assert header.is_jeans_visible()
        assert header.is_aerie_visible()
        assert header.is_clearance_visible()
        assert header.is_search_button_visible()