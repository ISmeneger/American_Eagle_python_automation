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