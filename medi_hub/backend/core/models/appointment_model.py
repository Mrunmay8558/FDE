from odmantic import Model, Field, ObjectId
from typing import Optional
from datetime import datetime, timezone
from pydantic import EmailStr, ConfigDict
from enum import Enum


class AppointmentStatus(str, Enum):
    """Defines the supported statuses that can be assigned to an appointment.

    Attributes:
        SCHEDULED: Appointment is scheduled and upcoming.
        COMPLETED: Appointment has occurred and is marked as completed.
        CANCELLED: Appointment was cancelled and will not occur.
    """

    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Appointment(Model):
    """Represents an appointment record stored by the application.

    Attributes:
        patient_id: ObjectId of the patient user associated with this appointment.
        doctor_id: ObjectId of the doctor user associated with this appointment.
        hospital_id: ObjectId of the hospital where the appointment is scheduled.
        appointment_datetime: Date and time when the appointment is scheduled to occur.
        reason_for_visit: Optional description of the reason for the appointment.
        appointment_status: Current status of the appointment (e.g., Scheduled, Completed, Cancelled).
        created_at: UTC timestamp indicating when the appointment record was created.
        updated_at: UTC timestamp indicating when the appointment record was last updated.
    """

    patient_id: ObjectId = Field(..., description="User ID of the patient")
    doctor_id: ObjectId = Field(..., description="User ID of the doctor")
    hospital_id: ObjectId = Field(
        ..., description="Hospital ID where the appointment is scheduled"
    )
    appointment_datetime: datetime = Field(
        ..., description="Date and time of the appointment"
    )
    reason_for_visit: Optional[str] = Field(
        None, description="Reason for the appointment"
    )
    appointment_status: AppointmentStatus = Field(
        default=AppointmentStatus.SCHEDULED,
        description="Status of the appointment (e.g., Scheduled, Completed, Cancelled)",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the appointment record was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the appointment record was last updated",
    )

    config = ConfigDict(
        collection="appointments",
        extra="forbid",
    )
