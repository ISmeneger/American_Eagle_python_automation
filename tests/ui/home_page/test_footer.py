import allure
import pytest

from ui.pages.home_page import HomePage


pytestmark = [
    pytest.mark.ui,
    pytest.mark.home_page,
]

COPYRIGHT_TEXT = "AEO Management Co. All Rights Reserved"


@pytest.mark.positive
@allure.feature("Home Page")
@allure.story("Footer")
@allure.title("Display footer content")
def test_footer_content_is_displayed_correctly(driver):
    home_page = HomePage(driver)

    with allure.step("Open American Eagle home page"):
        home_page.open()

    with allure.step("Scroll to copyright text"):
        home_page.footer.scroll_to_copyright_text()

    with allure.step("Verify copyright text"):
        assert (
            COPYRIGHT_TEXT
            in home_page.footer.get_copyright_text()
        )

    with allure.step("Scroll to footer image"):
        home_page.footer.scroll_to_footer_image()

    with allure.step("Verify footer image is visible"):
        assert home_page.footer.is_footer_image_visible()