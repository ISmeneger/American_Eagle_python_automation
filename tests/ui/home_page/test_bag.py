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
@allure.story("Shopping Bag")
@allure.title("Open Shopping Bag from header")
def test_shopping_bag_title_after_click(driver):
    home_page = HomePage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Open Shopping Bag from header"):
        home_page.header.click_bag_button()

    with allure.step("Verify Shopping Bag page title"):
        assert (
            home_page.header.get_bag_title_text()
            == "Shopping Bag"
        )