"""Main entrypoint to the API.

Apart from creating the API itself, additional code can be added to run at
startup.
"""
from my_tiny_service.api.api import get_api

main = get_api()
