from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.apis.schemas.requests.auth_request import UserAddress, UserRole


class UserResponse(BaseModel):
    """Represents a user entry returned by user listing endpoints.

    Attributes:
            id: String representation of the persisted MongoDB user ID.
            first_name: User's given name.
            last_name: User's family name.
            email: User's unique email address.
            mobile_number: User's primary contact phone number.
            user_address: Optional address information for the user.
            user_role: Role assigned to the user.
            user_metadata: Optional user-specific metadata.
            created_at: UTC timestamp for record creation.
            updated_at: UTC timestamp for last record update.
    """

    id: str = Field(..., description="String representation of the user ID")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: EmailStr = Field(..., description="User's email address")
    mobile_number: str = Field(..., description="User's mobile phone number")
    user_address: Optional[UserAddress] = Field(
        None, description="User's address information"
    )
    user_role: UserRole = Field(..., description="Role of the user in the system")
    user_metadata: Optional[dict] = Field(
        None, description="Additional metadata about the user"
    )
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when the user was last updated"
    )


class UsersListResponse(BaseModel):
    """Represents the API response returned after fetching all users.

    Attributes:
            message: Human-readable success message.
            users: Serialized list of user details.
    """

    message: str = Field(..., description="Success message for the list users request")
    users: list[UserResponse] = Field(..., description="List of user details")

    model_config = ConfigDict(extra="forbid")
