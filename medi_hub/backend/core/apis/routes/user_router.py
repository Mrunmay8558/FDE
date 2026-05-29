from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core import logger
from commons.auth import decodeJWT
from core.apis.schemas.responses.user_response import UserResponse, UsersListResponse
from core.controllers.user_controller import UserController

user_router = APIRouter()
logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


@user_router.get("/v1/users", response_model=UsersListResponse)
async def get_users(token: str = Depends(oauth2_scheme)):
    """
    Endpoint to fetch a list of users. This is a protected route that requires authentication.

    Args:
        token: The JWT token provided in the Authorization header.
    Returns:
        A list of users if the token is valid.
    Raises:
        HTTPException with status code 401 if the token is invalid or expired.
        HTTPException with status code 500 for any unexpected errors.
    """
    try:
        logging.info(f"Calling /v1/users endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if not authenticated_user_details:
            logging.warning(f"Invalid or expired token provided for fetching users")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        if authenticated_user_details.get("user_role") != "ADMIN":
            logging.warning(
                f"Unauthorized access attempt to /v1/users endpoint by user ID {authenticated_user_details.get('id')}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        result = await UserController().list_users()
        response = UsersListResponse(
            message="Users fetched successfully",
            users=[
                UserResponse(
                    **{
                        **user.model_dump(exclude={"password"}),
                        "id": str(user.id),
                    }
                )
                for user in result
            ],
        )
        return response.model_dump()
    except HTTPException as httperror:
        logging.error(f"Error in /v1/users endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/users endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )
