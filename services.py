from sqlalchemy.orm import Session

from . import models


def get_doctor(db: Session, doctor_id: int):
    return (
        db.query(models.Doctor)
        .filter(models.Doctor.id == doctor_id)
        .first()
    )


def get_patient(db: Session, patient_id: int):
    return (
        db.query(models.Patient)
        .filter(models.Patient.id == patient_id)
        .first()
    )


def check_doctor_for_assignment(
    db: Session,
    doctor_id: int
):
    doctor = get_doctor(db, doctor_id)

    if doctor is None:
        return None, "DOCTOR_NOT_FOUND"

    if not doctor.is_active:
        return None, "DOCTOR_INACTIVE"

    return doctor, None


def doctor_email_exists(
    db: Session,
    email: str,
    doctor_id: int | None = None
):
    query = db.query(models.Doctor).filter(
        models.Doctor.email == email
    )

    if doctor_id is not None:
        query = query.filter(
            models.Doctor.id != doctor_id
        )

    return query.first() is not None