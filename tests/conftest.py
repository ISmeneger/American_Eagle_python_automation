from pathlib import Path

import pytest
import requests

from api.client.bag_client import BagClient
from api.client.browse_client import BrowseClient
from api.client.inventory_client import InventoryClient


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

    environment_file = allure_results / "environment.properties"

    environment_file.write_text(
        "\n".join(
            [
                "Project=American Eagle Python Automation",
                "Language=Python 3.12.1",
                "Framework=Pytest",
                "HTTP_Client=requests",
                "OS=Windows 10",
                "Environment=Production",
                "Site=American Eagle",
            ]
        ),
        encoding="utf-8",
    )