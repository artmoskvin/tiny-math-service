import multiprocessing

import fastapi
import pytest
import starlette.testclient

from my_tiny_service.api.api import get_api

# Explicitly set start method to fork,
# https://github.com/pytest-dev/pytest-flask/issues/104
multiprocessing.set_start_method("fork")


@pytest.fixture()
def api() -> fastapi.FastAPI:
    """Fixture for the initialized API.

    It is useful to be able to access the api e.g., when doing dependency
    overrides.
    https://fastapi.tiangolo.com/advanced/testing-dependencies/
    """
    # Not sure why mypy cannot figure out the type unless explicitly given.
    api_instance: fastapi.FastAPI = get_api()
    return api_instance


@pytest.fixture()
def client(
    api: fastapi.FastAPI,
) -> starlette.testclient.TestClient:
    """Fixture for returning a starlette test client."""
    return starlette.testclient.TestClient(api)
