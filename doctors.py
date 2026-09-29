from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Doctor, Patient
from ..schemas import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
    PatientResponse
)
from ..auth.auth import (
    get_current_user,
    require_admin
)


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post(
    "",
    response_model=DoctorResponse
)
def create_doctor(
    data: DoctorCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    existing = db.query(Doctor).filter(
        Doctor.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    doctor = Doctor(
        name=data.name,
        specialization=data.specialization,
        email=data.email
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


@router.get(
    "",
    response_model=list[DoctorResponse]
)
def get_doctors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Doctor).filter(
        Doctor.is_active == True
    ).all()


@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def update_doctor(
    doctor_id: int,
    data: DoctorUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    updates = data.model_dump(
        exclude_unset=True
    )

    for key, value in updates.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.is_active = False

    db.commit()

    return {
        "message": "Doctor soft deleted successfully"
    }


@router.post(
    "/{doctor_id}/patients/{patient_id}"
)
def assign_patient(
    doctor_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if patient in doctor.patients:
        raise HTTPException(
            status_code=400,
            detail="Patient already assigned"
        )

    doctor.patients.append(patient)

    db.commit()

    return {
        "message": "Patient assigned successfully"
    }


@router.get(
    "/{doctor_id}/patients",
    response_model=list[PatientResponse]
)
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Doctor can only view their own patients
    if current_user.role == "doctor":

        linked_doctor = db.query(Doctor).filter(
            Doctor.email == current_user.email
        ).first()

        if not linked_doctor or linked_doctor.id != doctor_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own patients"
            )

    return doctor.patients