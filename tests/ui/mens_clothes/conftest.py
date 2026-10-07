import pytest

from ui.pages.home_page import HomePage
from ui.pages.jeans_page import JeansPage
from ui.pages.product_page import ProductPage
from ui.pages.shopping_cart_page import ShoppingCartPage
from ui.steps.product_catalog_steps import ProductCatalogSteps
from ui.steps.product_cart_steps import ProductCartSteps
from ui.pages.mens_clothes_page import MensClothesPage


@pytest.fixture
def home_page(driver):
    return HomePage(driver)


@pytest.fixture
def product_catalog_steps(driver):
    return ProductCatalogSteps(driver)


@pytest.fixture
def jeans_page(driver):
    return JeansPage(driver)


@pytest.fixture
def product_page(driver):
    return ProductPage(driver)


@pytest.fixture
def cart_page(driver):
    return ShoppingCartPage(driver)


@pytest.fixture
def product_cart_steps(driver):
    return ProductCartSteps(driver)


@pytest.fixture
def mens_clothes_page(driver):
    return MensClothesPage(driver)