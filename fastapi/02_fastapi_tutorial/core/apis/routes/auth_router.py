"""
auth_router.py

This router contains authentication endpoints such as register and login.

Teaching note:
- The router handles HTTP concerns only
- The controller handles business logic
- The CRUD layer is the first place that touches the shared database engine
    so the router stays simple for beginners
"""

from fastapi import APIRouter, HTTPException, status

from core import logger
from core.apis.schemas.requests.user_request import UserCreate, UserLogin
from core.apis.schemas.responses.user_responses import UserResponse, LoginResponse
from core.controllers.user_controller import UserController

logging = logger(__name__)

auth_router = APIRouter()


@auth_router.post(
    "/v1/auth/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def register_user(
    request: UserCreate,
):
    """
    Register a new user account.

    Args:
        request: Validated registration payload from UserCreate

    Returns:
        UserResponse: Newly created user data

    Raises:
        HTTPException: Re-raises controller validation errors or wraps
        unexpected exceptions as HTTP 500 responses.
    """
    try:
        logging.info("Calling /v1/auth/register endpoint")
        data = request.model_dump()
        return await UserController().create_user(user_data=data)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/auth/register endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/auth/register endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )


@auth_router.post(
    "/v1/auth/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
)
async def login_user(
    request: UserLogin,
):
    """
    Login a user using email and password.

    Args:
        request: Validated login payload from UserLogin

    Returns:
        LoginResponse: Access token and user profile data

    Raises:
        HTTPException: Re-raises known authentication errors or returns
        a 500 error for unexpected failures.
    """
    try:
        logging.info("Calling /v1/auth/login endpoint")
        return await UserController().login_user(
            email=request.email, password=request.password
        )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/auth/login endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/auth/login endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
