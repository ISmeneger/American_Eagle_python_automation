from api.client.token_client import TokenClient


def test_guest_token_received():
    token_client = TokenClient()

    response = token_client.get_guest_token_response()

    assert response.status_code == 200

    response_body = response.json()

    assert "access_token" in response_body
    assert response_body["access_token"]
    assert response_body["token_type"] == "Bearer"
    assert response_body["scope"] == "guest"