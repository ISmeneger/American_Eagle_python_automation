from ui.pages.account_page import AccountPage


class RegistrationSteps:

    def __init__(self, driver):
        self.account_page = AccountPage(driver)

    def fill_registration_form(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
    ):
        self.account_page.input_email(email)
        self.account_page.input_first_name(first_name)
        self.account_page.input_last_name(last_name)
        self.account_page.input_password(password)
        self.account_page.confirm_password(password)