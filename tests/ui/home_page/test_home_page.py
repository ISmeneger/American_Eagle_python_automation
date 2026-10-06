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
@allure.story("Home page availability")
@allure.title("Open American Eagle home page")
def test_home_page_opens(driver):
    home_page = HomePage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Verify home page is opened"):
        assert home_page.is_opened()