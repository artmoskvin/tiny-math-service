import fastapi
from starlette.middleware.cors import CORSMiddleware

from my_tiny_service.api.routers import maths, root
from my_tiny_service.api.settings import ApiSettings


def get_api() -> fastapi.FastAPI:
    """Create and set up the API.

    Register routers, middleware and similar to get a working API.
    """

    api_settings = ApiSettings()

    # Create the FastAPI class. All standard settings are configured in
    # setting.ApiSettings
    api = fastapi.FastAPI(
        title=api_settings.title,
        description=api_settings.description,
        version=api_settings.version,
        redoc_url=api_settings.redoc_url,
        openapi_url=api_settings.openapi_url,
        docs_url=api_settings.docs_url,
        servers=api_settings.servers,
    )

    # Save the settings in the API:s state so they can be retrieved when needed
    # by injecting a dependency on the utility function
    # spotify_fastapi_utils.get_api_settings in the path. See example in
    # routers/root.py
    api.state.api_settings = api_settings

    # Add CORS middleware, almost required if the API is to be used from a
    # browser. The CORS origins are configured in the settings.
    # https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
    api.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register the paths in the root router on the API.
    api.include_router(root.router)

    # Example endpoint doing simple maths arithmetic.
    # Routers can have a prefix, which is a very convenient way to do
    # versioning and custom response messages for status codes.
    #
    # Read more in the FastAPI docs
    # https://fastapi.tiangolo.com/tutorial/bigger-applications/
    # TODO: Investigate the mypy error from the line below
    api.include_router(
        maths.router, prefix="/v1/maths", responses=maths.responses  # type: ignore
    )

    return api
