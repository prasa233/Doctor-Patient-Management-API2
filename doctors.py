from fastapi import APIRouter

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.get("/")
def get_doctors():
    return {
        "message": "Doctors API is working"
    }


@router.get("/{doctor_id}")
def get_doctor(doctor_id: int):
    return {
        "doctor_id": doctor_id,
        "message": "Doctor found"
    }