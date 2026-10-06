import allure
import pytest

from api.config.settings import TEST_CATEGORY_ID


pytestmark = [
    pytest.mark.api,
    pytest.mark.browse,
]


@pytest.mark.smoke
@pytest.mark.positive
@allure.feature("Browse API")
@allure.story("Category products")
@allure.title("Get products from category")
def test_get_products_from_category(browse_client):
    response = browse_client.get_category_response(
        TEST_CATEGORY_ID
    )

    assert response.status_code == 200

    product_ids = browse_client.get_product_ids(
        TEST_CATEGORY_ID
    )

    assert product_ids
    assert len(product_ids) > 0


@pytest.mark.positive
@allure.feature("Browse API")
@allure.story("Category products")
@allure.title("Get random product ID from category")
def test_get_random_product_id(browse_client):
    product_id = browse_client.get_random_product_id(
        TEST_CATEGORY_ID
    )

    assert product_id

    print(
        "\nRandom product ID:",
        product_id,
    )


@pytest.mark.negative
@allure.feature("Browse API")
@allure.story("Category negative scenarios")
@allure.title("Request nonexistent category")
def test_get_nonexistent_category(browse_client):
    invalid_category_id = "cat999999999"

    with allure.step("Request nonexistent category"):
        response = browse_client.get_category_response(
            invalid_category_id
        )

    with allure.step(
        "Verify 404 response for nonexistent category"
    ):
        assert response.status_code == 404

        response_body = response.json()

        error = response_body["errors"][0]

        assert error["status"] == 404
        assert error["code"] == "error.browse.emptyProductList"
        assert error["title"] == "No Products Found"
        assert error["detail"] == "No Products Available"
        assert "categoryId" in error["meta"]["fields"]


@pytest.mark.negative
@allure.feature("Browse API")
@allure.story("Category negative scenarios")
@allure.title("Request category without Bearer token")
def test_get_category_without_authorization(browse_client):
    with allure.step(
        "Request category without Authorization"
    ):
        response = browse_client.get_category_response(
            TEST_CATEGORY_ID,
            include_authorization=False,
        )

    with allure.step(
        "Verify 401 response without Bearer token"
    ):
        assert response.status_code == 401

        response_body = response.json()

        assert response_body["error"]["status"] == "401"

        error = response_body["error"]["errors"][0]

        assert error["key"] == "apicg.token.invalid"