from pathlib import Path

import allure
import pytest
import requests

from api.client.bag_client import BagClient
from api.client.browse_client import BrowseClient
from api.client.inventory_client import InventoryClient
from api.client.token_client import TokenClient


@pytest.fixture
def api_session():
    session = requests.Session()

    yield session

    session.close()


@pytest.fixture
def browse_client(api_session):
    return BrowseClient(api_session)


@pytest.fixture
def inventory_client(api_session):
    return InventoryClient(api_session)


@pytest.fixture
def bag_client(api_session):
    return BagClient(api_session)


@pytest.fixture
def clean_bag(bag_client):
    response = bag_client.get_bag_response()

    assert response.status_code == 200

    bag = response.json()

    for item in bag["data"]["items"]:
        bag_client.delete_item(
            item_id=item["itemId"]
        )

    yield

    response = bag_client.get_bag_response()

    if response.status_code == 200:
        bag = response.json()

        for item in bag["data"]["items"]:
            bag_client.delete_item(
                item_id=item["itemId"]
            )


def pytest_sessionfinish(session, exitstatus):
    allure_results = Path("allure-results")
    allure_results.mkdir(exist_ok=True)

    environment_file = (
        allure_results / "environment.properties"
    )

    browser_name = getattr(
        session.config,
        "browser_name",
        "N/A",
    )

    browser_version = getattr(
        session.config,
        "browser_version",
        "N/A",
    )

    environment_file.write_text(
        "\n".join(
            [
                "Project=American Eagle Python Automation",
                "Language=Python 3.12.1",
                "Framework=Pytest",
                "HTTP_Client=requests",
                "Browser=" + browser_name,
                "Browser_Version=" + browser_version,
                "OS=Windows 10",
                "Environment=Production",
                "Site=American Eagle",
            ]
        ),
        encoding="utf-8",
    )


@pytest.fixture
def token_client(api_session):
    return TokenClient(api_session)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver")

    if driver is None:
        return

    allure.attach(
        driver.get_screenshot_as_png(),
        name="Screenshot on failure",
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        driver.current_url,
        name="Current URL",
        attachment_type=allure.attachment_type.TEXT,
    )
