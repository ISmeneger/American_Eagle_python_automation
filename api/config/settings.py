import os


BASE_URL = "https://www.ae.com"

GUEST_TOKEN_ENDPOINT = "/ugp-api/auth/oauth/v5/token"

BROWSE_CATEGORY_ENDPOINT = "/ugp-api/browse/v1/category/{category_id}"
TEST_CATEGORY_ID = "cat10025"

INVENTORY_ENDPOINT = "/ugp-api/inventory/v1/groupByProduct/US/{product_id}"

BAG_ENDPOINT = "/ugp-api/bag/v1"
BAG_ITEMS_ENDPOINT = "/ugp-api/bag/v1/items"

COMMON_HEADERS = {
    "Accept": "application/json",
    "aelang": "en_US",
    "aesite": "AEO_US",
    "aecountry": "US",
}


def get_guest_auth() -> str:
    guest_auth = os.getenv("AE_GUEST_AUTH")

    if not guest_auth:
        raise RuntimeError(
            "Environment variable AE_GUEST_AUTH is not set"
        )

    return guest_auth