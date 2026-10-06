import allure
import pytest

from ui.config import BASE_URL
from ui.constants import (
    MEN_PATH,
    MENS_CLOTHES_TITLE,
)
from ui.pages.home_page import HomePage
from ui.pages.mens_clothes_page import MensClothesPage


pytestmark = [
    pytest.mark.ui,
    pytest.mark.positive,
]


@allure.feature("Men's Clothes")
@allure.story("Men's catalog")
@allure.title("Open Men's Clothes page")
def test_mens_clothes_page_opens_correctly(driver):
    home_page = HomePage(driver)
    mens_clothes_page = MensClothesPage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Open Men's menu"):
        mens_clothes_page.move_to_men_menu()

    with allure.step("Click View All in Men's menu"):
        mens_clothes_page.click_view_all_categories()

    with allure.step("Close popup if available"):
        mens_clothes_page.close_popup_if_available()

    with allure.step("Verify Men's Clothes page title"):
        assert (
            mens_clothes_page.get_mens_page_title()
            == MENS_CLOTHES_TITLE
        )

    with allure.step("Verify Men's Clothes page URL"):
        assert (
            mens_clothes_page.get_current_url()
            == BASE_URL.rstrip("/") + MEN_PATH
        )