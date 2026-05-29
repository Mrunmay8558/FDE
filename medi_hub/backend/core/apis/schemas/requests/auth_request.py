from typing import Optional
from datetime import datetime, timezone
from pydantic import EmailStr, ConfigDict, BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    """Defines the supported roles that can be assigned to a user.

    Attributes:
        ADMIN: User with full administrative access.
        STAFF: User with internal staff-level access.
        USER: Standard application user.
        DOCTOR: User with doctor-specific access.
    """

    ADMIN = "ADMIN"
    STAFF = "STAFF"
    USER = "USER"
    DOCTOR = "DOCTOR"


class UserAddress(BaseModel):
    """Represents a user's address information.

    Attributes:
        street: Street address (e.g., "123 Main St").
        city: City name (e.g., "Springfield").
        state: State or province (e.g., "IL").
        postal_code: Postal or ZIP code (e.g., "62704").
        country: Country name (e.g., "USA").
    """

    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State or province")
    postal_code: str = Field(..., description="Postal or ZIP code")
    country: str = Field(..., description="Country name")


class UserCreateRequest(BaseModel):
    """Represents the data required to create a new user.

    Attributes:
        first_name: User's given name.
        last_name: User's family name.
        email: Unique email address used to identify the user.
        password: Plaintext password provided by the user (will be hashed before storage).
        mobile_number: User's primary contact phone number.

        user_address: Optional address information for the user.
    """

    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="Plaintext password for the user")
    mobile_number: str = Field(..., description="User's mobile phone number")
    user_address: UserAddress = Field(..., description="User's address information")


class UserLoginRequest(BaseModel):
    """Represents the data required for a user to log in.

    Attributes:
        email: The email address of the user attempting to log in.
        password: The plaintext password provided by the user for authentication.
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="Plaintext password for authentication")


class UserResetPasswordRequest(BaseModel):
    """Represents the data required for a user to reset their password.

    Attributes:
        old_password: The current plaintext password for authentication.
        new_password: The new plaintext password that the user wants to set.
    """

    old_password: str = Field(
        ..., description="Current plaintext password for authentication"
    )
    new_password: str = Field(..., description="New plaintext password for the user")


class UserUpdateRequest(BaseModel):
    """Represents the data that can be updated for an existing user.

    Attributes:
        first_name: User's given name.
        last_name: User's family name.
        mobile_number: User's primary contact phone number.
        user_address: Optional address information for the user.
    """

    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    mobile_number: Optional[str] = Field(None, description="User's mobile phone number")
    user_address: Optional[UserAddress] = Field(
        None, description="User's address information"
    )
    user_metdata: Optional[dict] = Field(
        None,
        description="Additional metadata about the user (e.g., preferences, settings)",
    )
    user_role: Optional[UserRole] = Field(
        None,
        description="Role of the user in the system (e.g., ADMIN, STAFF, USER, DOCTOR)",
    )
    password: Optional[str] = Field(
        None,
        description="Plaintext password for the user (will be hashed before storage)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the user record was last updated",
    )
