from fastapi import APIRouter, HTTPException, status
from core import logger
from core.apis.schemas.requests.auth_request import UserCreateRequest
from core.apis.schemas.responses.auth_response import SignupResponse, UserAuthResponse
from core.controllers.auth_controller import AuthController

auth_router = APIRouter()
logging = logger(__name__)


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
