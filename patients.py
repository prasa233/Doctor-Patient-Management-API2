from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import Patient, User
from app.schemas import (
    PatientCreate,
    PatientResponse
)
from fastapi import APIRouter

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
@router.get("/")
def get_patients():
    return {"message": "Patients API is working"}

from app.dependencies import (
    get_current_user,
    require_admin
)
from app.services.patient_service import (
    create_patient,
    get_patients,
    get_patient
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
def create(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return create_patient(db, data)


@router.get(
    "",
    response_model=list[PatientResponse]
)
def list_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role == "admin":
        return get_patients(db)

    # Doctor sees only assigned patients.
    if current_user.role == "doctor":

        return db.query(Patient).filter(
            Patient.doctor_id == current_user.id
        ).all()

    raise HTTPException(
        status_code=403,
        detail="Access denied"
    )


@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    patient = get_patient(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if current_user.role == "admin":
        return patient

    if (
        current_user.role == "doctor"
        and patient.doctor_id == current_user.id
    ):
        return patient

    raise HTTPException(
        status_code=403,
        detail="You can only view your assigned patients"
    )