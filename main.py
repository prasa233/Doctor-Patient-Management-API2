from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from app.database import Base, engine


from app.routes import (
    auth,
    doctors,
    patients,
    appointments
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Doctor Patient Management API",
    description="""
    Production-style Doctor and Patient Management API.

    Includes:
    - JWT Authentication
    - Role-based authorization
    - Doctor management
    - Patient management
    - Doctor-patient assignment
    - Appointment management
    - Validation
    - Pagination
    - Filtering
    """,
    version="2.0.0"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "details": exc.errors()
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(
    request: Request,
    exc: IntegrityError
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "Database constraint violation",
            "details": "The requested operation violates a database constraint."
        }
    )


@app.get("/")
def root():
    return {
        "message": "Doctor Patient API is running",
        "version": "2.0.0"
    }


app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)

from fastapi import FastAPI

from app .database import Base, engine
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Doctor Patient Management API",
    description="Production-style FastAPI Doctor and Patient Management System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Doctor Patient API is running"
    }