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
@allure.story("Account panel")
@allure.title("Display account panel content")
def test_account_panel_content(driver):
    home_page = HomePage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Open account panel"):
        home_page.header.click_account_button()

    with allure.step("Verify account panel content"):
        assert home_page.header.get_account_title_text() == "Account"
        assert home_page.header.is_sign_in_button_visible()
        assert home_page.header.is_create_account_button_visible()