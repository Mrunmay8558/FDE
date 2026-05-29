from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core import logger
from core.apis.schemas.requests.auth_request import (
    UserCreateRequest,
    UserLoginRequest,
    UserResetPasswordRequest,
)
from core.apis.schemas.responses.auth_response import SignupResponse, UserAuthResponse
from core.controllers.auth_controller import AuthController
from commons.auth import decodeJWT

auth_router = APIRouter()
logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


@auth_router.post("/v1/auth/signup", response_model=SignupResponse)
async def signup(request: UserCreateRequest):
    """
    User registration endpoint.

    Args:
        request: UserCreateRequest containing email, password, mobile number, and optional address.

    Returns:
        A success message if registration is successful.

    Raises:
        HTTPException with status code 400 if the email is already registered.
        HTTPException with status code 500 for any unexpected errors.
    """
    try:
        logging.info(f"Calling /v1/auth/signup endpoint")
        request = request.model_dump()
        result = await AuthController().signup(request=request)
        response = SignupResponse(
            message=result["message"],
            user=UserAuthResponse(**result["user"]),
        )
        return response.model_dump()
    except HTTPException as httperror:
        logging.error(f"Error in /v1/auth/signup endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/auth/signup endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )


@auth_router.post("/v1/auth/login")
async def login(request: UserLoginRequest):
    """
    User login endpoint.

    Args:
        request: UserLoginRequest containing email and password.

    Returns:
        A success message if login is successful along with user details and access token.

    Raises:
        HTTPException with status code 401 if authentication fails.
        HTTPException with status code 500 for any unexpected errors.
    """
    try:
        logging.info(f"Calling /v1/auth/login endpoint")
        request = request.model_dump()
        result = await AuthController().login(request=request)
        response = SignupResponse(
            message=result["message"],
            user=UserAuthResponse(**result["user"]),
        )
        return response.model_dump()
    except HTTPException as httperror:
        logging.error(f"Error in /v1/auth/login endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/auth/login endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )


@auth_router.post("/v1/auth/reset-password")
async def reset_password(
    request: UserResetPasswordRequest, token: str = Depends(oauth2_scheme)
):
    """
    User password reset endpoint.

    Args:
        request: UserResetPasswordRequest containing email and new password.
        token: JWT token for authentication.

    Returns:
        A success message if password reset is successful.

    Raises:
        HTTPException with status code 401 if authentication fails.
        HTTPException with status code 500 for any unexpected errors.
    """
    try:
        logging.info(f"Calling /v1/auth/reset-password endpoint")
        request = request.model_dump()
        authenticated_user_details = decodeJWT(token=token)
        if not authenticated_user_details:
            logging.warning(f"Invalid or expired token provided for password reset")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        result = await AuthController().reset_password(request=request, token=token)
        return {"message": result["message"]}
    except HTTPException as httperror:
        logging.error(f"Error in /v1/auth/reset-password endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/auth/reset-password endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )
