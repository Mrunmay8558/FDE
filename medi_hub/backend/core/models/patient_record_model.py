from odmantic import Model, Field, ObjectId
from typing import Optional
from datetime import datetime, timezone
from pydantic import EmailStr, ConfigDict
from enum import Enum


class PatientRecord(Model):
    """Represents a patient record stored by the application.

    Attributes:
        patient_id: ObjectId of the patient user associated with this record.
        medical_history: Optional list of past medical conditions or diagnoses.
        medications: Optional list of current medications the patient is taking.
        allergies: Optional list of known allergies the patient has.
        emergency_contact: Optional dictionary containing emergency contact
            information (e.g., name, relationship, phone number).
        created_at: UTC timestamp indicating when the patient record was created.
        updated_at: UTC timestamp indicating when the patient record was last
            updated.
    """

    patient_id: ObjectId = Field(..., description="User ID of the patient")
    appointment_id: ObjectId = Field(
        ..., description="Appointment ID associated with this record"
    )
    medical_history: Optional[list[str]] = Field(
        None, description="List of past medical conditions or diagnoses"
    )
    medications: Optional[list[str]] = Field(
        None, description="List of current medications the patient is taking"
    )
    allergies: Optional[list[str]] = Field(
        None, description="List of known allergies the patient has"
    )
    emergency_contact: Optional[dict] = Field(
        None,
        description="Emergency contact information (e.g., name, relationship, phone number)",
    )
    follow_up_date: Optional[datetime] = Field(
        None, description="Optional date for follow-up appointments or check-ins"
    )
    notes: Optional[str] = Field(
        None, description="Additional notes or comments about the patient"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the patient record was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the patient record was last updated",
    )

    config = ConfigDict(
        collection="patient_records",
        extra="forbid",
    )
