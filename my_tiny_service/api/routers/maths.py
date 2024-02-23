"""Endpoint examples with input/output models and error handling."""
import logging

import fastapi
import pydantic
import starlette.status

router = fastapi.APIRouter()
logger = logging.getLogger(__name__)

# Custom response descriptions for HTTP status codes. These responses are used
# when including the router in api.py.
#
# Read more in the FastAPI docs
# https://fastapi.tiangolo.com/tutorial/bigger-applications/
responses = {
    404: {"description": "Maths endpoint was not found"},
    200: {"description": "Calculation successful"},
}

# Pydantic models for the request body and response model.
#
# Read more in the FastAPI docs
# https://fastapi.tiangolo.com/tutorial/body/
# Pydantic is really nice for data validation and serialisation in general
# https://pydantic-docs.helpmanual.io/


class MathsBase(pydantic.BaseModel):
    number1: int
    number2: int


class MathsResult(MathsBase):
    """Result model features the operation as well as the result value."""

    operation: str
    result: int | float


class MathsIn(MathsBase):
    pass


@router.post(
    "/addition",
    summary="Calculate the sum of two numbers",
    response_model=MathsResult,
)
def addition(maths_input: MathsIn) -> MathsResult:
    """Calculates the sum of two whole numbers."""
    return MathsResult(
        **maths_input.dict(),
        operation="addition",
        result=maths_input.number1 + maths_input.number2,
    )


@router.post(
    "/multiplication",
    summary="Calculate the product of two numbers",
    response_model=MathsResult,
)
def multiplication(maths_input: MathsIn) -> MathsResult:
    """Calculates the product of two whole numbers."""
    return MathsResult(
        **maths_input.dict(),
        operation="multiplication",
        result=maths_input.number1 * maths_input.number2,
    )


@router.post(
    "/subtraction",
    summary="Calculate the difference of two numbers",
    response_model=MathsResult,
)
def subtraction(maths_input: MathsIn) -> MathsResult:
    """Calculates the difference of two whole numbers."""
    return MathsResult(
        **maths_input.dict(),
        operation="subtraction",
        result=maths_input.number1 - maths_input.number2,
    )


@router.post(
    "/division",
    summary="Calculate the quotient of two numbers",
    response_model=MathsResult,
    # This endpoint raises a HTTPException with a 400 status code. That code is
    # not automatically included in the OpenAPI spec. For strict schema
    # compliance it needs to be defined in the responses argument.
    responses={"400": {"description": "Division by zero is not allowed"}},
)
def division(maths_input: MathsIn) -> MathsResult:
    """Calculates the quotient of two whole numbers.

    Raises HTTP 400 Bad request if division by zero is attempted. Prefer to
    raise explicit exception rather than having the code fail (which will give a
    500 Internal server error). Note that the status codes needs to be added to
    the responses argument in the path.
    """
    try:
        return MathsResult(
            **maths_input.dict(),
            operation="division",
            result=maths_input.number1 / maths_input.number2,
        )
    except ZeroDivisionError as e:
        logger.debug("Someone tried to divide by zero", exc_info=True)
        raise fastapi.HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail="Division by zero is not allowed",
        ) from e
