import allure
import pytest

from ui.pages.home_page import HomePage


pytestmark = [
    pytest.mark.ui,
    pytest.mark.home_page,
]

FAVORITES_TITLE = "Favorites"


@pytest.mark.smoke
@pytest.mark.positive
@allure.feature("Home Page")
@allure.story("Favorites")
@allure.title("Open Favorites page from header")
def test_favorites_title_after_click(driver):
    home_page = HomePage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Open Favorites from header"):
        home_page.header.click_favorites_button()

    with allure.step("Verify Favorites page title"):
        assert (
            home_page.header.get_favorites_title_text()
            == FAVORITES_TITLE
        )