from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from fastapi import FastAPI

app = FastAPI()

from app.database import get_db
from app.dependencies import (
    get_current_user,
    require_admin
)

from app.models import (
    Appointment,
    Doctor,
    Patient,
    User
)

from app.schemas import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=201
)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Doctor is inactive"
        )

    patient = db.query(Patient).filter(
        Patient.id == data.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if patient.doctor_id != doctor.id:
        raise HTTPException(
            status_code=400,
            detail="Patient is not assigned to this doctor"
        )

    overlapping = db.query(Appointment).filter(
        Appointment.doctor_id == data.doctor_id,
        Appointment.appointment_date == data.appointment_date,
        Appointment.status == "scheduled"
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=409,
            detail="Doctor already has an appointment at this time"
        )

    appointment = Appointment(
        doctor_id=data.doctor_id,
        patient_id=data.patient_id,
        appointment_date=data.appointment_date,
        status=data.status,
        created_by=current_user.id,
        updated_by=current_user.id
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment


@router.get(
    "",
    response_model=list[AppointmentResponse]
)
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Appointment)

    if current_user.role == "doctor":

        if not current_user.doctor:
            raise HTTPException(
                status_code=403,
                detail="Doctor profile not linked"
            )

        query = query.filter(
            Appointment.doctor_id == current_user.doctor.id
        )

    return query.order_by(
        Appointment.appointment_date
    ).all()


@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if current_user.role == "doctor":

        if appointment.doctor_id != current_user.doctor.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    return appointment


@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def update_appointment(
    appointment_id: int,
    data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    values = data.model_dump(
        exclude_unset=True
    )

    doctor_id = values.get(
        "doctor_id",
        appointment.doctor_id
    )

    patient_id = values.get(
        "patient_id",
        appointment.patient_id
    )

    appointment_date = values.get(
        "appointment_date",
        appointment.appointment_date
    )

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Doctor is inactive"
        )

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if patient.doctor_id != doctor_id:
        raise HTTPException(
            status_code=400,
            detail="Patient is not assigned to this doctor"
        )

    overlap = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.status == "scheduled",
        Appointment.id != appointment_id
    ).first()

    if overlap:
        raise HTTPException(
            status_code=409,
            detail="Doctor already has an appointment at this time"
        )

    for field, value in values.items():
        setattr(appointment, field, value)

    appointment.updated_by = current_user.id

    db.commit()
    db.refresh(appointment)

    return appointment


@router.delete(
    "/{appointment_id}"
)
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }