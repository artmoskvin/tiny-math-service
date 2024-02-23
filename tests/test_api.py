"""Examples testing the api using the starlette TestClient.

The test fixture "client" is defined in conftest.py
These tests are trivial examples, they are not meant as an introduction to
proper testing.

Read more about testing in the FastAPI docs:
https://fastapi.tiangolo.com/tutorial/testing/
"""

import starlette.testclient


def test_read_root(client: starlette.testclient.TestClient) -> None:
    """Test that the root path can be read."""

    # GIVEN the root path
    path = "/"

    # WHEN calling the api
    response = client.get(path)

    # THEN status_code should be 200
    assert response.status_code == 200


def test_addition(client: starlette.testclient.TestClient) -> None:
    """Test that the addition endpoint correctly sums two numbers."""

    # GIVEN the addition path and two numbers to sum
    path = "/v1/maths/addition"
    body = {"number1": 2, "number2": 3}

    # WHEN calling the api
    response = client.post(path, json=body)

    # THEN the sum should be 5
    assert response.json().get("result") == 5


def test_divide_by_zero(client: starlette.testclient.TestClient) -> None:
    """Test that the division endpoint returns a 400 when dividing by 0."""

    # GIVEN the division path and two numbers to divide
    path = "/v1/maths/division"
    body = {"number1": 2, "number2": 0}

    # WHEN calling the api
    response = client.post(path, json=body)

    # THEN the status code should be 400 (Bad request)
    assert response.status_code == 400
