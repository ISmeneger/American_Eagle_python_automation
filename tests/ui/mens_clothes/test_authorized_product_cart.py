import allure
import pytest


pytestmark = [
    pytest.mark.ui,
    pytest.mark.positive,
]


ANTI_BOT_SIGN_IN_REASON = (
    "Automated sign-in is blocked by the site's anti-bot "
    "protection. Manual sign-in works successfully."
)


@allure.feature("Men's Clothes")
@allure.story("Authorized Shopping Bag")
@allure.title(
    "Authorized user adds a product to Shopping Bag"
)
@pytest.mark.skip(reason=ANTI_BOT_SIGN_IN_REASON)
def test_authorized_user_adds_product_to_cart():
    pass