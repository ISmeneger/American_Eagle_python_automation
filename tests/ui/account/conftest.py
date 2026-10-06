import pytest

from ui.pages.account_page import AccountPage
from ui.pages.home_page import HomePage
from ui.steps.registration_steps import RegistrationSteps


@pytest.fixture
def registration_context(driver):
    home_page = HomePage(driver)
    account_page = AccountPage(driver)
    registration_steps = RegistrationSteps(driver)

    home_page.open()

    home_page.header.click_account_button()
    home_page.header.click_create_account_button()

    return {
        "account_page": account_page,
        "registration_steps": registration_steps,
    }


@pytest.fixture
def sign_in_page(driver):
    home_page = HomePage(driver)
    account_page = AccountPage(driver)

    home_page.open()

    home_page.header.click_account_button()
    home_page.header.click_sign_in_button()

    return account_page