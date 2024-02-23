from starlette.requests import Request

from my_tiny_service.api.settings import ApiSettings


def get_api_settings(request: Request) -> ApiSettings:
    return request.app.state.api_settings  # type: ignore[no-any-return]
