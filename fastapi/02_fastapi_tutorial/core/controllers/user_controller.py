"""
user_controller.py — Business logic layer for user operations.

Architecture:
  Router (HTTP layer) → Controller (business logic) → CRUD (database layer)

Controllers:
  - Are NOT aware of HTTP details (no Request/Response objects here)
  - Contain all business rules: validation, password hashing, token creation
  - Call one or more CRUD methods to persist / retrieve data
  - Call utility helpers (email, password generation, etc.)
  - Raise HTTPException so the router can return the right status code

This keeps routes thin (just call controller, return result) and
makes business logic easy to unit-test without HTTP overhead.
"""

import secrets
import string
from fastapi import HTTPException, status

from core.cruds.user_crud import CRUDUser
from core.models.user_model import UserStatus
from commons.auth import encrypt_password, verify_password, signJWT
from core.utils.email.email_helper import send_email
from core.utils.email.email_template_generator import welcome_email_with_credentials
from core import logger

logging = logger(__name__)


def _generate_random_password(length: int = 12) -> str:
    """Generate a random alphanumeric password for auto-created accounts."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class UserController:
    """
    Handles all business logic for user-related operations.

    Instantiate once per request (FastAPI's default DI behaviour):
        controller = UserController()
        result = await controller.create_user(data)
    """

    def __init__(self):
        self.crud_user = CRUDUser()

    # ------------------------------------------------------------------
    # CREATE USER
    # ------------------------------------------------------------------

    async def create_user(self, user_data: dict) -> dict:
        """
        Register a new user account.

        Steps:
          1. Check email uniqueness
          2. Generate a random password
          3. Hash the password before storage (NEVER store plain text)
          4. Save user with PENDING_VERIFICATION status
          5. Send welcome email with the temporary credentials
          6. Return success response with access token

        Args:
            user_data: Dict from UserCreate schema (first_name, last_name, email, mobile_number)

        Returns:
            dict: user details + access_token

        Raises:
            HTTPException 400: email already registered
            HTTPException 500: DB error or email sending failed
        """
        try:
            logging.info(f"UserController.create_user: {user_data.get('email')}")

            # 1. Email uniqueness check
            existing = await self.crud_user.get_by_email(email=user_data["email"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this email already exists.",
                )

            # 2. Generate random temporary password
            plain_password = _generate_random_password()

            # 3. Hash password
            hashed = encrypt_password(plain_password)

            # 4. Build user document and save
            db_user = await self.crud_user.create(
                obj_in={
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "email": user_data["email"],
                    "mobile_number": user_data.get("mobile_number"),
                    "hashed_password": hashed,
                    "status": UserStatus.PENDING_VERIFICATION,
                },
            )

            # 5. Send welcome email with credentials
            try:
                email_data = welcome_email_with_credentials(
                    name=db_user.first_name,
                    email=db_user.email,
                    password=plain_password,
                )
                await send_email(
                    subject=email_data["subject"],
                    to_email=db_user.email,
                    text=email_data["text"],
                    html=email_data["html"],
                )
            except Exception as email_err:
                logging.warning(f"Welcome email failed (non-fatal): {email_err}")

            # 6. Issue access token
            access_token = signJWT(user_role=db_user.role, id=str(db_user.id))

            return {
                "id": str(db_user.id),
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "email": db_user.email,
                "mobile_number": db_user.mobile_number,
                "role": db_user.role,
                "status": db_user.status,
                "created_at": db_user.created_at,
                "access_token": access_token,
            }

        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"UserController.create_user error: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user.",
            )

    # ------------------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------------------

    async def login_user(self, email: str, password: str) -> dict:
        """
        Authenticate user with email + password.

        Steps:
          1. Look up user by email
          2. Verify the bcrypt hash matches the supplied password
          3. Check account status is ACTIVE
          4. Return access token

        Raises:
            HTTPException 401: Invalid credentials or account not active
        """
        try:
            logging.info(f"UserController.login_user: {email}")

            user = await self.crud_user.get_by_email(email=email)
            if not user or not verify_password(password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password.",
                )

            if user.status != UserStatus.ACTIVE:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Account is {user.status}. Please verify your email.",
                )

            access_token = signJWT(user_role=user.role, id=str(user.id))

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": str(user.id),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "mobile_number": user.mobile_number,
                    "role": user.role,
                    "status": user.status,
                    "created_at": user.created_at,
                },
            }

        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"UserController.login_user error: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed due to an internal error.",
            )

    # ------------------------------------------------------------------
    # GET PROFILE
    # ------------------------------------------------------------------

    async def get_user_profile(self, user_id: str) -> dict:
        """
        Fetch the authenticated user's profile.

        Args:
            user_id: ObjectId string from the decoded JWT

        Raises:
            HTTPException 404: User not found
        """
        try:
            user = await self.crud_user.get_by_id(id=user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found.",
                )
            return {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "mobile_number": user.mobile_number,
                "role": user.role,
                "status": user.status,
                "created_at": user.created_at,
            }
        except HTTPException:
            raise
        except Exception as error:
            logging.error(f"UserController.get_user_profile error: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch user profile.",
            )
