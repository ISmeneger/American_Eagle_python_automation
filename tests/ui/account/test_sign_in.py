import allure
import pytest


pytestmark = [
    pytest.mark.ui,
    pytest.mark.account,
]


EMAIL_VALIDATION_MESSAGE = (
    "Please enter a valid email address."
)


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Sign In")
@allure.title("Sign in with invalid email")
def test_sign_in_with_invalid_email(sign_in_page):
    with allure.step("Enter invalid email"):
        sign_in_page.input_email("invalid-email")

    with allure.step("Click Continue"):
        sign_in_page.click_continue_button()

    with allure.step("Verify invalid email validation message"):
        assert sign_in_page.is_invalid_email_error_visible()
        assert (
            sign_in_page.get_invalid_email_error_message()
            == EMAIL_VALIDATION_MESSAGE
        )


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Sign In")
@allure.title("Sign in with empty email")
def test_sign_in_with_empty_email(sign_in_page):
    with allure.step("Leave email field empty"):
        sign_in_page.input_email("")

    with allure.step("Click Continue"):
        sign_in_page.click_continue_button()

    with allure.step("Verify invalid email validation message"):
        assert sign_in_page.is_invalid_email_error_visible()
        assert (
            sign_in_page.get_invalid_email_error_message()
            == EMAIL_VALIDATION_MESSAGE
        )


@pytest.mark.positive
@allure.feature("Account")
@allure.story("Sign In")
@allure.title("Successful sign in")
@pytest.mark.skip(
    reason=(
        "Automated sign-in is blocked by the site's anti-bot "
        "protection. Manual sign-in works successfully."
    )
)
def test_successful_sign_in():
    pass


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Sign In")
@allure.title("Sign in with invalid password")
@pytest.mark.skip(
    reason=(
        "Password validation cannot be reached reliably "
        "because automated sign-in is blocked by anti-bot protection."
    )
)
def test_sign_in_with_invalid_password():
    pass


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Sign In")
@allure.title("Sign in with empty password")
@pytest.mark.skip(
    reason=(
        "Password validation cannot be reached reliably "
        "because automated sign-in is blocked by anti-bot protection."
    )
)
def test_sign_in_with_empty_password():
    pass


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Sign In")
@allure.title("Sign in with short password")
@pytest.mark.skip(
    reason=(
        "Password validation cannot be reached reliably "
        "because automated sign-in is blocked by anti-bot protection."
    )
)
def test_sign_in_with_short_password():
    pass


@pytest.mark.negative
@allure.feature("Account")
@allure.story("Sign In")
@allure.title("Sign in with long password")
@pytest.mark.skip(
    reason=(
        "Password validation cannot be reached reliably "
        "because automated sign-in is blocked by anti-bot protection."
    )
)
def test_sign_in_with_long_password():
    pass