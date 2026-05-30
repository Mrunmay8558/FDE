from odmantic import Model, Field, ObjectId
from typing import Optional
from datetime import datetime, timezone
from pydantic import EmailStr, ConfigDict
from enum import Enum
from pydantic import BaseModel


class HosptialAddress(BaseModel):
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


class Hospital(Model):
    """Represents a hospital record stored by the application.

    Attributes:
        hospital_name: Official name of the hospital.
        hospital_address: Physical address of the hospital.
        hospital_email: Contact email address for the hospital.
        hospital_phone: Primary contact phone number for the hospital.
        hospital_website: Optional official website URL.
        hospital_services: Optional list of medical services offered by the
            hospital.
        hospital_metadata: Optional dictionary containing additional hospital
            details such as metadata, ratings, or extended configuration.
        hospital_working_hours: Optional working hours or operating schedule
            for the hospital.
        hospital_working_days: Optional list of days on which the hospital is
            open or operating.
        created_by: ObjectId of the user who created the hospital record.
        created_at: UTC timestamp indicating when the hospital record was
            created.
        updated_at: UTC timestamp indicating when the hospital record was last
            updated.
    """

    hospital_name: str = Field(..., description="Name of the hospital")
    hospital_address: HosptialAddress = Field(..., description="Address of the hospital")
    hospital_email: EmailStr = Field(..., description="Contact email for the hospital")
    hospital_phone: str = Field(
        ..., description="Contact phone number for the hospital"
    )
    hospital_website: Optional[str] = Field(
        None, description="Official website URL for the hospital"
    )
    hospital_services: Optional[list[str]] = Field(
        None,
        description="List of medical services offered by the hospital (e.g., Cardiology, Pediatrics)",
    )
    hospital_metadata: Optional[dict] = Field(
        None,
        description="Additional metadata about the hospital (e.g., services offered, ratings)",
    )
    hospital_working_hours: Optional[str] = Field(
        None, description="List of working hours for the hospital"
    )
    hospital_working_days: Optional[list[str]] = Field(
        None, description="List of working days for the hospital"
    )
    created_by: ObjectId = Field(
        ..., description="User ID of the creator of this hospital record"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the hospital record was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the hospital record was last updated",
    )

    config = ConfigDict(
        collection="hospitals",
        extra="forbid",
    )
