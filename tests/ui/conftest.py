
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver(pytestconfig):
    options = Options()

    # Disable geolocation and browser notifications.
    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2,
        },
    )

    # Do not wait for all page resources to finish loading.
    options.page_load_strategy = "eager"

    is_ci = os.getenv("CI", "").lower() == "true"

    # Configure headless Chrome for GitHub Actions.
    if is_ci:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # Maximize browser window during local UI testing.
        if not is_ci:
            driver.maximize_window()

        # Save browser information for Allure environment metadata.
        pytestconfig.browser_name = driver.capabilities.get(
            "browserName",
            "Unknown",
        )

        pytestconfig.browser_version = driver.capabilities.get(
            "browserVersion",
            "Unknown",
        )

        yield driver

    finally:
        # Always close the browser after the test.
        driver.quit()
