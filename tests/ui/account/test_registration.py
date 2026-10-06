import allure
import pytest


from utils.test_data_generator import (
    generate_email,
    generate_first_name,
    generate_last_name,
    generate_password,
)


pytestmark = [
    pytest.mark.ui,
    pytest.mark.account,
]


POSTAL_CODE = "07008"
MONTH_VALUE = "August"
DAY_VALUE = "21"

EMAIL_VALIDATION_MESSAGE = "Please enter a valid email address."
EMPTY_PASSWORD_MESSAGE = "Please enter your password."
EMPTY_FIRST_NAME_MESSAGE = "Please enter your first name."
EMPTY_LAST_NAME_MESSAGE = "Please enter your last name."
EMPTY_POSTAL_CODE_MESSAGE = "Please enter your zip/postal code."


@pytest.mark.negative
@pytest.mark.parametrize(
    "email",
    [
        "user.gmail.com",
        "",
    ],
)
@allure.feature("Account")
@allure.story("Registration")
@allure.title("Validate email during account registration")
def test_registration_email_validation(
    registration_context,
    email,
):
    account_page = registration_context["account_page"]
    registration_steps = registration_context["registration_steps"]

    first_name = generate_first_name()
    last_name = generate_last_name()
    password = generate_password()

    with allure.step("Fill registration form"):
        registration_steps.fill_registration_form(
            email,
            first_name,
            last_name,
            password,
        )

    with allure.step("Fill additional registration data"):
        account_page.input_zip_code(POSTAL_CODE)
        account_page.select_birth_date(
            MONTH_VALUE,
            DAY_VALUE,
        )
        account_page.scroll_to_submit_button()
        account_page.accept_terms_and_conditions()

    with allure.step("Verify email validation"):
        assert not account_page.is_submit_account_button_enabled()
        assert account_page.is_email_validation_error_visible()
        assert (
            account_page.get_email_validation_error_message()
            == EMAIL_VALIDATION_MESSAGE
        )


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Registration")
@allure.title("Register with empty first and last name")
def test_registration_with_empty_name_fields(
    registration_context,
):
    account_page = registration_context["account_page"]
    registration_steps = registration_context["registration_steps"]

    email = generate_email()
    password = generate_password()

    with allure.step("Fill registration form with empty name fields"):
        registration_steps.fill_registration_form(
            email,
            "",
            "",
            password,
        )

    with allure.step("Fill additional registration data"):
        account_page.input_zip_code(POSTAL_CODE)
        account_page.select_birth_date(
            MONTH_VALUE,
            DAY_VALUE,
        )
        account_page.scroll_to_submit_button()
        account_page.accept_terms_and_conditions()

    with allure.step("Verify validation for empty name fields"):
        assert not account_page.is_submit_account_button_enabled()

        assert account_page.is_empty_first_name_error_visible()
        assert (
            account_page.get_empty_first_name_error_message()
            == EMPTY_FIRST_NAME_MESSAGE
        )

        assert account_page.is_empty_last_name_error_visible()
        assert (
            account_page.get_empty_last_name_error_message()
            == EMPTY_LAST_NAME_MESSAGE
        )


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Registration")
@allure.title("Register with empty password")
def test_registration_with_empty_password(
    registration_context,
):
    account_page = registration_context["account_page"]
    registration_steps = registration_context["registration_steps"]

    email = generate_email()
    first_name = generate_first_name()
    last_name = generate_last_name()

    with allure.step("Fill registration form with empty password"):
        registration_steps.fill_registration_form(
            email,
            first_name,
            last_name,
            "",
        )

    with allure.step("Fill additional registration data"):
        account_page.input_zip_code(POSTAL_CODE)
        account_page.select_birth_date(
            MONTH_VALUE,
            DAY_VALUE,
        )
        account_page.scroll_to_submit_button()
        account_page.accept_terms_and_conditions()

    with allure.step("Verify empty password validation"):
        assert not account_page.is_submit_account_button_enabled()
        assert account_page.is_empty_password_error_visible()
        assert (
            account_page.get_empty_password_error_message()
            == EMPTY_PASSWORD_MESSAGE
        )


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Registration")
@allure.title("Register with empty zip code")
def test_registration_with_empty_zip_code(
    registration_context,
):
    account_page = registration_context["account_page"]
    registration_steps = registration_context["registration_steps"]

    email = generate_email()
    first_name = generate_first_name()
    last_name = generate_last_name()
    password = generate_password()

    with allure.step("Fill registration form"):
        registration_steps.fill_registration_form(
            email,
            first_name,
            last_name,
            password,
        )

    with allure.step("Leave zip code empty and fill remaining data"):
        account_page.input_zip_code("")
        account_page.select_birth_date(
            MONTH_VALUE,
            DAY_VALUE,
        )
        account_page.scroll_to_submit_button()
        account_page.accept_terms_and_conditions()

    with allure.step("Verify zip code validation"):
        assert not account_page.is_submit_account_button_enabled()
        assert account_page.is_empty_zip_code_error_visible()
        assert (
            account_page.get_empty_zip_code_error_message()
            == EMPTY_POSTAL_CODE_MESSAGE
        )


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Registration")
@allure.title("Register without birth date and terms acceptance")
def test_registration_without_birth_date_and_terms(
    registration_context,
):
    account_page = registration_context["account_page"]
    registration_steps = registration_context["registration_steps"]

    email = generate_email()
    first_name = generate_first_name()
    last_name = generate_last_name()
    password = generate_password()

    with allure.step("Fill registration form"):
        registration_steps.fill_registration_form(
            email,
            first_name,
            last_name,
            password,
        )

    with allure.step("Fill zip code without birth date and terms"):
        account_page.input_zip_code(POSTAL_CODE)
        account_page.scroll_to_submit_button()

    with allure.step("Verify form cannot be submitted"):
        assert not account_page.is_terms_checkbox_selected()
        assert not account_page.is_submit_account_button_enabled()


@pytest.mark.positive
@pytest.mark.defect
@allure.feature("Account")
@allure.story("Registration")
@allure.title("Successful account creation")
@pytest.mark.skip(
    reason=(
        "Automated account creation is blocked by the site's anti-bot "
        "protection. Registration form filling works, but submission "
        "results in Access Denied."
    )
)
def test_successful_account_creation():
    pass