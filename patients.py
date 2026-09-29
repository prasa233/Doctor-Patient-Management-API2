from app.models import Appointment
from app.schemas import AppointmentResponse

@router.get(
    "/{patient_id}/appointments",
    response_model=list[AppointmentResponse]
)
def get_patient_appointments(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if current_user.role == "doctor":

        if patient.doctor_id != current_user.doctor.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    return (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .order_by(Appointment.appointment_date)
        .all()
    )


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import (
    get_current_user,
    require_admin
)

from app.models import Patient, Doctor, User
from app.schemas import (
    PatientCreate,
    PatientUpdate,
    PatientResponse
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=201
)
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    if data.doctor_id:

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
                detail="Cannot assign patient to inactive doctor"
            )

    patient = Patient(
        name=data.name,
        age=data.age,
        phone=data.phone,
        doctor_id=data.doctor_id,
        created_by=current_user.id,
        updated_by=current_user.id
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


@router.get(
    "",
    response_model=list[PatientResponse]
)
def list_patients(
    age_gt: int | None = Query(default=None, gt=0),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Patient)

    if current_user.role == "doctor":

        if not current_user.doctor:
            raise HTTPException(
                status_code=403,
                detail="Doctor profile not linked"
            )

        query = query.filter(
            Patient.doctor_id == current_user.doctor.id
        )

    if age_gt:
        query = query.filter(
            Patient.age > age_gt
        )

    offset = (page - 1) * limit

    return (
        query
        .order_by(Patient.id)
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if current_user.role == "doctor":

        if patient.doctor_id != current_user.doctor.id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your assigned patients"
            )

    return patient


@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def update_patient(
    patient_id: int,
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if data.doctor_id:

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

    patient.name = data.name
    patient.age = data.age
    patient.phone = data.phone
    patient.doctor_id = data.doctor_id
    patient.updated_by = current_user.id

    db.commit()
    db.refresh(patient)

    return patient


@router.patch(
    "/{patient_id}",
    response_model=PatientResponse
)
def patch_patient(
    patient_id: int,
    data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if data.doctor_id:

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

    for field, value in data.model_dump(
        exclude_unset=True
    ).items():
        setattr(patient, field, value)

    patient.updated_by = current_user.id

    db.commit()
    db.refresh(patient)

    return patient


@router.delete(
    "/{patient_id}"
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patient.is_active = False
    patient.updated_by = current_user.id

    db.commit()

    return {
        "message": "Patient soft deleted successfully"
    }