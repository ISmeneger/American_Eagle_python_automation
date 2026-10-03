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