import allure
import pytest


pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
]


@pytest.mark.smoke
@pytest.mark.positive
@allure.feature("Authentication API")
@allure.story("Guest token")
@allure.title("Receive guest access token")
def test_guest_token_received(token_client):
    with allure.step("Request guest access token"):
        response = token_client.get_guest_token_response()

    with allure.step("Verify successful token response"):
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["access_token"]
        assert response_body["token_type"] == "Bearer"
        assert response_body["scope"] == "guest"
        assert response_body["expires_in"] > 0


@pytest.mark.negative
@allure.feature("Authentication API")
@allure.story("Guest token negative scenarios")
@allure.title("Request guest token without Authorization header")
def test_guest_token_without_authorization(token_client):
    with allure.step("Request guest token without Authorization"):
        response = token_client.request_guest_token(
            authorization=None
        )

    with allure.step("Verify request is rejected"):
        assert response.status_code == 401


@pytest.mark.negative
@allure.feature("Authentication API")
@allure.story("Guest token negative scenarios")
@allure.title("Request guest token with invalid Authorization")
def test_guest_token_with_invalid_authorization(token_client):
    with allure.step("Request guest token with invalid credentials"):
        response = token_client.request_guest_token(
            authorization="Basic invalid_credentials"
        )

    with allure.step("Verify request is rejected"):
        assert response.status_code == 401