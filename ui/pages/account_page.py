from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class AccountPage(BasePage):

    CREATE_ACCOUNT_BUTTON = (
        By.XPATH,
        "//a[@data-test='register-button']"
    )

    EMAIL_INPUT = (
        By.XPATH,
        "//input[@placeholder='Email']"
    )

    CONTINUE_BUTTON = (
        By.ID,
        "kc-login"
    )

    PASSWORD_SIGN_IN_METHOD = (
        By.ID,
        "PASSWORD"
    )

    ERROR_WARNING = (
        By.CSS_SELECTOR,
        "h6.alert-header"
    )

    INVALID_PASSWORD_ERROR = (
        By.CSS_SELECTOR,
        "div[data-label-code='error.account.login.passwordInvalid']"
    )

    INVALID_EMAIL_ERROR = (
        By.XPATH,
        "//span[contains(@class,'kc-feedback-text') "
        "and normalize-space()='Please enter a valid email address.']"
    )

    FIRST_NAME_INPUT = (
        By.ID,
        "firstName"
    )

    LAST_NAME_INPUT = (
        By.ID,
        "lastName"
    )

    PASSWORD_INPUT = (
        By.ID,
        "password"
    )

    CONFIRM_PASSWORD_INPUT = (
        By.ID,
        "password-confirm"
    )

    ZIP_CODE_INPUT = (
        By.ID,
        "postalCode"
    )

    BIRTH_MONTH = (
        By.ID,
        "birthMonth"
    )

    BIRTH_DAY = (
        By.ID,
        "birthDay"
    )

    TERMS_CHECKBOX = (
        By.ID,
        "termsAccepted"
    )

    SUBMIT_ACCOUNT_BUTTON = (
        By.ID,
        "kc-register-button"
    )

    EMPTY_FIRST_NAME_ERROR = (
        By.XPATH,
        "//input[@id='firstName']/"
        "following-sibling::span[contains(@class,'kc-feedback-text')]"
    )

    EMPTY_LAST_NAME_ERROR = (
        By.XPATH,
        "//input[@id='lastName']/"
        "following-sibling::span[contains(@class,'kc-feedback-text')]"
    )

    EMPTY_PASSWORD_ERROR = (
        By.XPATH,
        "//input[@id='password']/following-sibling::span"
        "[contains(@class,'kc-feedback-text')]"
    )

    EMPTY_ZIP_CODE_ERROR = (
        By.XPATH,
        "//input[@id='postalCode']/"
        "following-sibling::span[contains(@class,'kc-feedback-text')]"
    )

    EMAIL_VALIDATION_ERROR = (
        By.XPATH,
        "//input[@id='email']/"
        "following-sibling::span[contains(@class,'kc-feedback-text')]"
    )

    def _type_into_field(self, locator, value: str):
        field = self.wait_for_clickable(locator)
        field.clear()
        field.send_keys(value)

    def input_email(self, email: str):
        field = self.wait_for_clickable(self.EMAIL_INPUT)
        field.clear()
        field.send_keys(email)

    def click_continue_button(self):
        self.click(self.CONTINUE_BUTTON)

    def select_password_sign_in_method(self):
        self.click(self.PASSWORD_SIGN_IN_METHOD)

    def get_login_warning_error(self) -> str:
        return self.get_text(self.ERROR_WARNING)

    def is_login_warning_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_WARNING)

    def get_invalid_password_error(self) -> str:
        return self.get_text(self.INVALID_PASSWORD_ERROR)

    def is_invalid_password_error_visible(self) -> bool:
        return self.is_visible(self.INVALID_PASSWORD_ERROR)

    def get_invalid_email_error(self) -> str:
        return self.get_text(self.INVALID_EMAIL_ERROR)

    def is_invalid_email_error_visible(self) -> bool:
        return self.is_visible(self.INVALID_EMAIL_ERROR)

    def get_invalid_email_error_message(self) -> str:
        return self.get_text(self.INVALID_EMAIL_ERROR)

    def input_first_name(self, first_name: str):
        self._type_into_field(
            self.FIRST_NAME_INPUT,
            first_name,
        )

    def input_last_name(self, last_name: str):
        self._type_into_field(
            self.LAST_NAME_INPUT,
            last_name,
        )

    def input_password(self, password: str):
        self._type_into_field(
            self.PASSWORD_INPUT,
            password,
        )

    def confirm_password(self, password: str):
        self._type_into_field(
            self.CONFIRM_PASSWORD_INPUT,
            password,
        )

    def input_zip_code(self, zip_code: str):
        self._type_into_field(
            self.ZIP_CODE_INPUT,
            zip_code,
        )

    def select_birth_month(self, value: str):
        dropdown = self.wait_for_clickable(
            self.BIRTH_MONTH
        )

        Select(dropdown).select_by_value(value)

    def select_birth_day(self, value: str):
        dropdown = self.wait_for_clickable(
            self.BIRTH_DAY
        )

        Select(dropdown).select_by_value(value)

    def select_birth_date(
            self,
            month: str,
            day: str,
    ):
        self.select_birth_month(month)
        self.select_birth_day(day)

    def scroll_to_submit_button(self):
        button = self.wait_for_visible(
            self.SUBMIT_ACCOUNT_BUTTON
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button,
        )

    def accept_terms_and_conditions(self):
        checkbox = self.wait_for_present(
            self.TERMS_CHECKBOX
        )

        if not checkbox.is_selected():
            self.driver.execute_script(
                "arguments[0].click();",
                checkbox,
            )

    def is_terms_checkbox_selected(self) -> bool:
        checkbox = self.wait_for_present(
            self.TERMS_CHECKBOX
        )

        return checkbox.is_selected()

    def is_submit_account_button_enabled(self) -> bool:
        return self.wait_for_visible(
            self.SUBMIT_ACCOUNT_BUTTON
        ).is_enabled()

    def is_email_validation_error_visible(self) -> bool:
        return self.is_visible(
            self.EMAIL_VALIDATION_ERROR
        )

    def get_email_validation_error_message(self) -> str:
        return self.get_text(
            self.EMAIL_VALIDATION_ERROR
        )

    def is_empty_password_error_visible(self) -> bool:
        return self.is_visible(
            self.EMPTY_PASSWORD_ERROR
        )

    def get_empty_password_error_message(self) -> str:
        return self.get_text(
            self.EMPTY_PASSWORD_ERROR
        )

    def is_empty_first_name_error_visible(self) -> bool:
        return self.is_visible(
            self.EMPTY_FIRST_NAME_ERROR
        )

    def get_empty_first_name_error_message(self) -> str:
        return self.get_text(
            self.EMPTY_FIRST_NAME_ERROR
        )

    def is_empty_last_name_error_visible(self) -> bool:
        return self.is_visible(
            self.EMPTY_LAST_NAME_ERROR
        )

    def get_empty_last_name_error_message(self) -> str:
        return self.get_text(
            self.EMPTY_LAST_NAME_ERROR
        )

    def is_empty_zip_code_error_visible(self) -> bool:
        return self.is_visible(
            self.EMPTY_ZIP_CODE_ERROR
        )

    def get_empty_zip_code_error_message(self) -> str:
        return self.get_text(
            self.EMPTY_ZIP_CODE_ERROR
        )