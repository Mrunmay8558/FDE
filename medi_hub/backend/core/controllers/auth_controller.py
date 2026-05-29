from fastapi import HTTPException, status
from core import logger
from core.cruds.auth_crud import CRUDAuth
from commons.auth import signJWT, encrypt_password, verify_password

logging = logger(__name__)


class AuthController:
    """
    Controller for authentication and user management related operations, such as registration, login, password reset, etc.
    """

    def __init__(self):
        self.crud_auth = CRUDAuth()

    async def signup(self, request: dict):
        """
        Handle user registration.

        Args:
            request: A dictionary containing user registration details such as email, password, mobile number, and optional address.

        Returns:
            A success message if registration is successful.

        Raises:
            HTTPException with status code 400 if the email is already registered.
            HTTPException with status code 500 for any unexpected errors.
        """
        try:
            logging.info(f"Executing AuthController.signup function")
            user = await self.crud_auth.get_by_email(email=request.get("email", ""))
            if user:
                logging.warning(f"Email {request.get('email')} is already registered")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is already registered",
                )
            hashed_password = encrypt_password(request.get("password", ""))
            request["password"] = hashed_password
            saved_user = await self.crud_auth.create(obj_in=request)
            if not saved_user:
                logging.error(
                    f"Failed to create user with email {request.get('email')}"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user",
                )
            logging.info(f"User with email {request.get('email')} created successfully")
            access_token = signJWT(
                user_role=saved_user.user_role.value,
                id=str(saved_user.id),
                expiry_duration=86400,
            )
            saved_user_dict = saved_user.model_dump()
            saved_user_dict["id"] = str(saved_user.id)
            saved_user_dict["access_token"] = access_token
            saved_user_dict.pop("password", None)
            return {
                "message": "User registered successfully",
                "user": saved_user_dict,
            }

        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in AuthController.signup function: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )

    async def login(self, request: dict):
        """
        Handle user login.

        Args:
            request: A dictionary containing user login details such as email and password.

        Returns:
            A success message if login is successful along with user details and access token.

        Raises:
            HTTPException with status code 401 if authentication fails.
            HTTPException with status code 500 for any unexpected errors.
        """
        try:
            logging.info(f"Executing AuthController.login function")
            user = await self.crud_auth.get_by_email(email=request.get("email", ""))
            if not user:
                logging.warning(
                    f"Authentication failed for email {request.get('email')}"
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found with the provided email",
                )
            if not verify_password(request.get("password", ""), user.password):
                logging.warning(
                    f"Authentication failed for email {request.get('email')}"
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )
            access_token = signJWT(
                user_role=user.user_role.value,
                id=str(user.id),
                expiry_duration=86400,
            )
            user_dict = user.model_dump()
            user_dict["id"] = str(user.id)
            user_dict["access_token"] = access_token
            user_dict.pop("password", None)
            logging.info(
                f"User with email {request.get('email')} logged in successfully"
            )
            return {
                "message": "Login successful",
                "user": user_dict,
            }

        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in AuthController.login function: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )

    async def reset_password(self, request: dict, authenticated_user_details: dict):
        """
        Handle user password reset.

        Args:
            request: A dictionary containing old_password and new_password.
            authenticated_user_details: A dictionary containing details of the authenticated user (e.g., user ID).

        Returns:
            A success message if password reset is successful.

        Raises:
            HTTPException with status code 401 if authentication fails.
            HTTPException with status code 500 for any unexpected errors.
        """
        try:
            logging.info(f"Executing AuthController.reset_password function")
            user_id = authenticated_user_details.get("id")
            user = await self.crud_auth.get(id=user_id)
            if not user:
                logging.warning(f"User with ID {user_id} not found for password reset")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            if not verify_password(request.get("old_password", ""), user.password):
                logging.warning(
                    f"Authentication failed for user ID {user_id} during password reset"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid current password",
                )
            new_hashed_password = encrypt_password(request.get("new_password", ""))
            update_data = {"password": new_hashed_password}
            await self.crud_auth.update(id=user_id, obj_in=update_data)
            logging.info(f"Password reset successful for user ID {user_id}")
            return {"message": "Password reset successful"}

        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in AuthController.reset_password function: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )
