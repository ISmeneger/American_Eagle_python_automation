import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ui.pages.base_page import BasePage


@pytest.fixture
def driver(pytestconfig):
    options = Options()

    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2,
        }
    )

    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    pytestconfig.browser_name = driver.capabilities.get(
        "browserName",
        "Unknown",
    )
    pytestconfig.browser_version = driver.capabilities.get(
        "browserVersion",
        "Unknown",
    )

    yield driver

    try:
        BasePage(driver).close_popup_if_available()
    except Exception:
        pass

    driver.quit()