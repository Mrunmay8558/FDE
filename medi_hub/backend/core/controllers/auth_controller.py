import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from core import logger
from core.cruds.auth_crud import CRUDAuth
from commons.auth import (
    signJWT,
    encrypt_password,
    verify_password,
    generate_otp,
    hash_otp,
    verify_hashed_otp,
)
from core.apis.schemas.requests.auth_request import OtpPurpose
from core.utils.email.email_helper import send_email
from core.utils.email.email_template_generator import generate_email_template

logging = logger(__name__)

OTP_EXPIRY_SECONDS = 30
OTP_REQUEST_INTERVAL_SECONDS = 30
MAX_OTP_ATTEMPTS = 5
OTP_ATTEMPT_WINDOW_SECONDS = 3600


class AuthController:
    """
    Controller for authentication and user management related operations, such as registration, login, password reset, etc.
    """

    def __init__(self):
        self.crud_auth = CRUDAuth()

    async def _clear_otp_state(self, user_id):
        await self.crud_auth.update(
            id=user_id,
            obj_in={"otp": None},
        )

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
            request["email"] = request.get("email", "").strip().lower()
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
            return {
                "message": "User registered successfully",
                "user": {
                    **saved_user.model_dump(exclude={"password", "otp"}),
                    "id": str(saved_user.id),
                    "access_token": signJWT(
                        user_role=saved_user.user_role.value,
                        id=str(saved_user.id),
                        expiry_duration=86400,
                    ),
                },
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
            request["email"] = request.get("email", "").strip().lower()
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
            logging.info(
                f"User with email {request.get('email')} logged in successfully"
            )
            return {
                "message": "Login successful",
                "user": {
                    **user.model_dump(exclude={"password", "otp"}),
                    "id": str(user.id),
                    "access_token": signJWT(
                        user_role=user.user_role.value,
                        id=str(user.id),
                        expiry_duration=86400,
                    ),
                },
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

    async def request_otp(self, request: dict):
        """
        Generate and email an OTP for login or forgot-password flows.

        Args:
            request: A dictionary containing the user's email and OTP purpose.

        Returns:
            A success message including the OTP purpose and expiry duration.

        Raises:
            HTTPException with status code 404 if the user is not found.
            HTTPException with status code 429 if an OTP was requested too recently.
            HTTPException with status code 500 if OTP generation, persistence, or email sending fails.
        """
        try:
            logging.info(f"Executing AuthController.request_otp function")
            request["email"] = request.get("email", "").strip().lower()
            purpose = request.get("purpose", "")
            purpose_value = purpose.value if isinstance(purpose, OtpPurpose) else str(purpose)
            purpose_label = purpose_value.replace("_", " ").title()
            user = await self.crud_auth.get_by_email(email=request.get("email", ""))
            if not user:
                logging.warning(
                    f"OTP requested for unregistered email {request.get('email')}"
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found with the provided email",
                )

            now = datetime.now(timezone.utc)
            if user.otp:
                elapsed_seconds = (now - user.otp.requested_at).total_seconds()
                if elapsed_seconds < OTP_REQUEST_INTERVAL_SECONDS:
                    retry_after = int(OTP_REQUEST_INTERVAL_SECONDS - elapsed_seconds)
                    logging.warning(
                        f"OTP requested too frequently for email {request.get('email')}"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=(
                            "Please wait "
                            f"{retry_after} seconds before requesting another OTP"
                        ),
                    )

            otp = generate_otp()
            expires_at = now + timedelta(seconds=OTP_EXPIRY_SECONDS)
            await self.crud_auth.update(
                id=user.id,
                obj_in={
                    "otp": {
                        "code_hash": hash_otp(otp),
                        "purpose": purpose_value,
                        "expires_at": expires_at,
                        "requested_at": now,
                        "attempt_count": 0,
                        "attempt_window_started_at": now,
                    },
                },
            )

            template = generate_email_template(
                name=user.first_name,
                subject=f"{purpose_label} OTP for MediHub",
                title="Your OTP Code",
                description=(
                    f"Use this OTP to complete the {purpose_label.lower()} flow. "
                    f"It expires in {OTP_EXPIRY_SECONDS} seconds."
                ),
                action_code=otp,
            )

            try:
                await send_email(
                    subject=template["subject"],
                    to_email=user.email,
                    text=template["text"],
                    html=template["html"],
                )
            except Exception as error:
                logging.error(
                    f"Failed to send OTP email for {request.get('email')}: {error}"
                )
                await self._clear_otp_state(user.id)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to send OTP email",
                )

            logging.info(
                f"OTP sent successfully for email {request.get('email')} and purpose {purpose_value}"
            )
            return {
                "message": f"OTP sent successfully for {purpose_label.lower()}",
                "purpose": purpose_value,
                "expires_in_seconds": OTP_EXPIRY_SECONDS,
            }

        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in AuthController.request_otp function: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )

    async def verify_otp(self, request: dict):
        """
        Verify a shared OTP endpoint and branch by purpose inside the controller.

        Args:
            request: A dictionary containing email, OTP, purpose, and optional new_password.

        Returns:
            A login success response with user details when the OTP purpose is LOGIN.
            A password reset success message when the OTP purpose is FORGOT_PASSWORD.

        Raises:
            HTTPException with status code 400 if the OTP is invalid, expired, missing, or the request is incomplete.
            HTTPException with status code 404 if the user is not found.
            HTTPException with status code 429 if the OTP attempt limit for the active window is exceeded.
            HTTPException with status code 500 for any unexpected errors.
        """
        try:
            logging.info(f"Executing AuthController.verify_otp function")
            request["email"] = request.get("email", "").strip().lower()
            purpose = request.get("purpose", "")
            purpose_value = purpose.value if isinstance(purpose, OtpPurpose) else str(purpose)
            user = await self.crud_auth.get_by_email(email=request.get("email", ""))
            if not user:
                logging.warning(
                    f"OTP verification attempted for unregistered email {request.get('email')}"
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found with the provided email",
                )

            if not user.otp or user.otp.purpose.value != purpose_value:
                logging.warning(
                    f"No active OTP found for email {request.get('email')} and purpose {purpose_value}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No active OTP found for the requested purpose",
                )

            now = datetime.now(timezone.utc)
            if user.otp.expires_at < now:
                logging.warning(f"Expired OTP used for email {request.get('email')}")
                await self._clear_otp_state(user.id)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="OTP has expired. Please request a new OTP",
                )

            if (now - user.otp.attempt_window_started_at).total_seconds() >= OTP_ATTEMPT_WINDOW_SECONDS:
                await self.crud_auth.update(
                    id=user.id,
                    obj_in={
                        "otp": {
                            **user.otp.model_dump(),
                            "attempt_count": 0,
                            "attempt_window_started_at": now,
                        }
                    },
                )
                user = await self.crud_auth.get_by_email(email=request.get("email", ""))

            if user.otp.attempt_count >= MAX_OTP_ATTEMPTS:
                logging.warning(
                    f"OTP attempt limit reached for email {request.get('email')}"
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="OTP attempt limit exceeded for the current 1 hour window",
                )

            if not verify_hashed_otp(request.get("otp", ""), user.otp.code_hash):
                next_attempt_count = user.otp.attempt_count + 1
                await self.crud_auth.update(
                    id=user.id,
                    obj_in={
                        "otp": {
                            **user.otp.model_dump(),
                            "attempt_count": next_attempt_count,
                        }
                    },
                )

                if next_attempt_count >= MAX_OTP_ATTEMPTS:
                    detail = "OTP attempt limit exceeded for the current 1 hour window"
                else:
                    detail = (
                        f"Invalid OTP. {MAX_OTP_ATTEMPTS - next_attempt_count} attempts remaining"
                    )

                logging.warning(
                    f"Invalid OTP submitted for email {request.get('email')} and purpose {purpose_value}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=detail,
                )

            if purpose_value == OtpPurpose.LOGIN.value:
                await self._clear_otp_state(user.id)
                logging.info(
                    f"OTP login successful for email {request.get('email')}"
                )
                return {
                    "message": "Login successful",
                    "user": {
                        **user.model_dump(exclude={"password", "otp"}),
                        "id": str(user.id),
                        "access_token": signJWT(
                            user_role=user.user_role.value,
                            id=str(user.id),
                            expiry_duration=86400,
                        ),
                    },
                }

            if purpose_value == OtpPurpose.FORGOT_PASSWORD.value:
                new_password = request.get("new_password", "")
                if not new_password:
                    logging.warning(
                        f"Forgot-password OTP verified without new password for email {request.get('email')}"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="new_password is required for forgot-password flow",
                    )

                await self.crud_auth.update(
                    id=user.id,
                    obj_in={"password": encrypt_password(new_password)},
                )
                await self._clear_otp_state(user.id)
                logging.info(
                    f"Password updated successfully using OTP for email {request.get('email')}"
                )
                return {"message": "Password reset successful"}

            logging.warning(f"Unsupported OTP purpose received: {purpose_value}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported OTP purpose",
            )

        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"Error in AuthController.verify_otp function: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )
