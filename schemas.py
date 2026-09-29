from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator
)


# =========================
# AUTH
# =========================

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)
    role: str = "doctor"

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        if value not in ["admin", "doctor"]:
            raise ValueError("Role must be admin or doctor")
        return value


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================
# DOCTOR
# =========================

class DoctorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    specialization: str = Field(min_length=2, max_length=100)
    email: EmailStr


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# PATIENT
# =========================

class PatientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^\d{10}$")
    doctor_id: Optional[int] = None


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^\d{10}$"
    )
    doctor_id: Optional[int] = None
    is_active: Optional[bool] = None


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: Optional[int]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# PAGINATION
# =========================

class PaginationResponse(BaseModel):
    total_records: int
    current_page: int
    limit: int


# =========================
# APPOINTMENTS
# =========================

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: str = "scheduled"

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        allowed = [
            "scheduled",
            "completed",
            "cancelled"
        ]

        if value not in allowed:
            raise ValueError(
                "Status must be scheduled, completed or cancelled"
            )

        return value


class AppointmentUpdate(BaseModel):
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value is None:
            return value

        allowed = [
            "scheduled",
            "completed",
            "cancelled"
        ]

        if value not in allowed:
            raise ValueError(
                "Status must be scheduled, completed or cancelled"
            )

        return value


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# ERROR RESPONSE
# =========================

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Optional[object] = None