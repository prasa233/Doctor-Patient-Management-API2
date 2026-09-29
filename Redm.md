# Doctor–Patient FastAPI Project 

## Objective

Enhance the existing FastAPI application with authorization, appointments, data integrity, performance, auditing, reliability, testing, and documentation.

###  Role-Based Authorization

* Add JWT roles: `admin`, `doctor`.
* Admin: full Doctor and Patient access.
* Doctor: view only assigned patients.
* Doctor cannot delete Doctors or Patients.
* Unauthorized operations must return `403 Forbidden`.

###  Appointment Module

Create Appointment management.

**Fields**

* `id`
* `doctor_id`
* `patient_id`
* `appointment_date`
* `status`: `scheduled`, `completed`, `cancelled`

**Validation**

* Doctor and Patient must exist.
* Doctor must be active.
* Prevent overlapping appointments for the same Doctor.

**APIs**

* Appointment CRUD
* `GET /doctors/{doctor_id}/appointments`
* `GET /patients/{patient_id}/appointments`

###  Data Integrity

* Unique DB constraint on Doctor email.
* Foreign-key constraints for relationships.
* Handle database exceptions.
* Return meaningful error messages instead of raw DB errors.

###  Performance

* Optimize SQLAlchemy queries.
* Prevent N+1 query problems.
* Add indexes where required.
* Measure list API response time.

### Audit & Tracking

Add:

* `created_at`
* `updated_at`
* `created_by`
* `updated_by`

Requirements:

* Get user information from JWT.
* Automatically maintain timestamps.
* Track users who create/update records.

### Level 16 – API Hardening

* Global exception handling.
* Consistent custom error responses.
* Uniform validation-error handling.
* Basic API rate limiting.

**Example:**

```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have permission to perform this operation"
  }
}
```

### Level 17 – Testing & Coverage

**Unit Tests**

* Services
* Validation
* Authorization
* Appointment overlap logic

**API Tests**

* Register/Login
* JWT authentication
* Admin permissions
* Doctor permissions
* Appointment APIs

**Coverage**

* Minimum: `70%`

Recommended:

* `pytest`
* `pytest-cov`
* `httpx`

### Level 18 – Documentation

Enhance Swagger/OpenAPI documentation with:

* API descriptions
* Authentication requirements
* Request examples
* Response examples
* Error responses
* Role/permission details

Swagger:
`/docs`

ReDoc:
`/redoc`

## Submission Requirements

* [ ] Levels 11–18 implemented
* [ ] JWT role-based authorization
* [ ] Appointment module
* [ ] Database constraints
* [ ] Query optimization
* [ ] Audit tracking
* [ ] Exception handling
* [ ] Rate limiting
* [ ] Automated tests
* [ ] Minimum 70% coverage
* [ ] Swagger documentation
* [ ] README
* [ ] Swagger/Postman screenshots
* [ ] Working project with requirements file

## Expected Deliverables

```text
doctor_patient_api1/
├── app/
├── tests/
├── requirements.txt
├── README.md
├── redmin.md
└── screenshots/
    ├── swagger.png
    └── postman.png
```
