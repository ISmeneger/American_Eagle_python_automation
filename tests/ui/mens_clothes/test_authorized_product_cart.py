import allure
import pytest


pytestmark = [
    pytest.mark.ui,
    pytest.mark.positive,
    pytest.mark.defect,
]


@allure.feature("Men's Clothes")
@allure.story("Authorized Shopping Bag")
@allure.title(
    "Authorized user adds a product to Shopping Bag"
)
@pytest.mark.skip(
    reason=(
        "Automated sign-in is blocked by the site's anti-bot "
        "protection. Manual sign-in works successfully."
    )
)
def test_authorized_user_adds_product_to_cart():
    pass