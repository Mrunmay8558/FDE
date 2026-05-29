"""
user_router.py

This router contains user profile endpoints.

Teaching note:
- Authentication is checked in the router because this is where request
    headers are available
- The controller is called only after the JWT has been validated
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core import logger
from core.apis.schemas.responses.user_responses import UserResponse
from core.controllers.user_controller import UserController
from commons.auth import decodeJWT

logging = logger(__name__)
user_router = APIRouter()

# FastAPI reads the Bearer token from the Authorization header automatically.
# tokenUrl points to the login endpoint shown in the OpenAPI docs.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


@user_router.get(
    "/v1/auth/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_me(
    token: str = Depends(oauth2_scheme),
):
    """
    Return the profile of the currently authenticated user.

    This endpoint reads the Bearer token from the Authorization header,
    decodes the JWT, extracts the user ID, and then asks the controller
    for the matching user profile.

    Args:
        token: Bearer token extracted automatically by OAuth2PasswordBearer

    Returns:
        UserResponse: Authenticated user's profile

    Raises:
        HTTPException: 401 for invalid token, 404 for missing user,
        or 500 for unexpected failures.
    """
    try:
        logging.info("Calling /v1/auth/me endpoint")

        # The token is already extracted from the Authorization header,
        # so it can be decoded directly.
        authenticated_user_details = decodeJWT(token)

        if not authenticated_user_details:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )

        user_id = authenticated_user_details.get("id")
        return await UserController().get_user_profile(user_id=user_id)

    except HTTPException as httperror:
        logging.error(f"Error in /v1/auth/me endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/auth/me endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
