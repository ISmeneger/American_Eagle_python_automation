import pytest

from ui.pages.home_page import HomePage
from ui.pages.product_page import ProductPage
from ui.pages.shopping_cart_page import ShoppingCartPage
from ui.steps.product_cart_steps import ProductCartSteps


@pytest.fixture
def home_page(driver):
    return HomePage(driver)


@pytest.fixture
def product_page(driver):
    return ProductPage(driver)


@pytest.fixture
def cart_page(driver):
    return ShoppingCartPage(driver)


@pytest.fixture
def product_cart_steps(driver):
    return ProductCartSteps(driver)