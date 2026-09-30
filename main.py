from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.database import Base, engine
from app.router.doctors import router as doctor_router
from app.router.patients import router as patient_router
from fastapi import FastAPI
from fastapi import FastAPI

from app.router.doctors import router as doctor_router


app = FastAPI(
    title="Doctor Patient Management API"
)


app.include_router(doctor_router)


@app.get("/")
def root():
    return {
        "message": "Doctor Patient API is running"
    }
app = FastAPI(
    title="Doctor Patient Management API",
    description="FastAPI backend for managing doctors and patients",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Doctor Patient Management API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(doctor_router)


app = FastAPI(
    title="Doctor Patient Management API",
    description="FastAPI backend for managing doctors and patients",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(patient_router)


@app.get("/")
def root():

    return {
        "message": "Doctor Patient API is running"
    }