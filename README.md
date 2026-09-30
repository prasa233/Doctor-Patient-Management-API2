# Hospital Management API

## Billing Module

The Billing module manages patient billing associated
with doctors and appointments.

### Billing Flow

Patient
   ↓
Doctor
   ↓
Appointment
   ↓
Billing
   ↓
Payment

### Billing APIs

POST   /billings
GET    /billings/{billing_id}
GET    /patients/{patient_id}/billings
GET    /doctors/{doctor_id}/billings
PUT    /billings/{billing_id}
PATCH  /billings/{billing_id}
DELETE /billings/{billing_id}

### Payment Status

pending
paid
cancelled

### Payment Mode

cash
card
upi

### Business Rules

1. Patient must exist.
2. Doctor must exist.
3. Doctor must be active.
4. Appointment must match patient and doctor.
5. Cancelled appointments cannot be billed.
6. One appointment cannot have duplicate active billing.
7. Total amount is calculated by the backend.
8. Billing deletion is implemented as soft delete.