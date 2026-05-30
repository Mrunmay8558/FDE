from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core import logger
from core.apis.schemas.requests.auth_request import (
    UserCreateRequest,
    UserLoginRequest,
    RequestOtpRequest,
    UserResetPasswordRequest,
    VerifyOtpRequest,
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
        result = await AuthController().signup(request=request.model_dump())
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


@auth_router.post("/v1/auth/login", response_model=SignupResponse)
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
        result = await AuthController().login(request=request.model_dump())
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


@auth_router.post("/v1/auth/request-otp")
async def request_otp(request: RequestOtpRequest):
    """
    Shared endpoint to request an email OTP for supported authentication flows.

    Args:
        request: RequestOtpRequest containing the user's email address and OTP purpose.

    Returns:
        A success message indicating that the OTP was sent, along with purpose and expiry details.

    Raises:
        HTTPException with status code 404 if the user does not exist.
        HTTPException with status code 429 if an OTP was requested too recently.
        HTTPException with status code 500 for any unexpected errors.
    """
    try:
        logging.info(f"Calling /v1/auth/request-otp endpoint")
        result = await AuthController().request_otp(request=request.model_dump())
        return result
    except HTTPException as httperror:
        logging.error(f"Error in /v1/auth/request-otp endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/auth/request-otp endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )


@auth_router.post("/v1/auth/verify-otp")
async def verify_otp(request: VerifyOtpRequest):
    """
    Shared endpoint to verify OTPs for login and forgot-password flows.

    Args:
        request: VerifyOtpRequest containing email, OTP, purpose, and optional new password.

    Returns:
        A login response with user details if the OTP purpose is LOGIN.
        A success message if the OTP purpose is FORGOT_PASSWORD and the password reset succeeds.

    Raises:
        HTTPException with status code 400 if the OTP is invalid, expired, or the request is incomplete.
        HTTPException with status code 404 if the user does not exist.
        HTTPException with status code 429 if the OTP attempt limit is exceeded.
        HTTPException with status code 500 for any unexpected errors.
    """
    try:
        logging.info(f"Calling /v1/auth/verify-otp endpoint")
        result = await AuthController().verify_otp(request=request.model_dump())
        if result.get("user"):
            response = SignupResponse(
                message=result["message"],
                user=UserAuthResponse(**result["user"]),
            )
            return response.model_dump()
        return result
    except HTTPException as httperror:
        logging.error(f"Error in /v1/auth/verify-otp endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/auth/verify-otp endpoint: {error}")
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
        result = await AuthController().reset_password(
            request=request,
            authenticated_user_details=authenticated_user_details,
        )
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
