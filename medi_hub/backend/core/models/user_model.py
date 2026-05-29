from odmantic import Model, Field
from typing import Optional
from datetime import datetime, timezone
from pydantic import EmailStr, ConfigDict, BaseModel
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


class User(Model):
    """Represents a user record stored in the users collection.

    Attributes:
        first_name: User's given name.
        last_name: User's family name.
        email: Unique email address used to identify the user.
        password: Hashed password stored for authentication.
        mobile_number: User's primary contact phone number.
        user_role: Role assigned to the user. Supported values are
            ``UserRole.ADMIN``, ``UserRole.STAFF``, ``UserRole.USER``, and
            ``UserRole.DOCTOR``.
        user_metadata: Optional dictionary containing extra user-specific
            metadata such as preferences or settings.
        created_at: UTC timestamp indicating when the user record was created.
        updated_at: UTC timestamp indicating when the user record was last
            updated.
    """

    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: EmailStr = Field(..., description="User's email address", unique=True)
    password: str = Field(..., description="Hashed password")
    mobile_number: str = Field(..., description="User's mobile phone number")
    user_address: Optional[UserAddress] = Field(
        None, description="User's address information"
    )
    user_role: UserRole = Field(
        default=UserRole.USER, description="Role of the user in the system"
    )
    user_metadata: Optional[dict] = Field(
        None,
        description="Additional metadata about the user (e.g., preferences, settings)",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the user was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the user was last updated",
    )

    model_config = ConfigDict(
        collection="users",  # MongoDB collection name
        extra="forbid",  # Forbid extra fields not defined in the model
    )
