from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


# ---------------------
# PATIENT
# ---------------------
class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    age: int = Field(..., gt=0, lt=120)


class PatientResponse(PatientCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------
# VITAL SIGNS
# ---------------------
class VitalSignsCreate(BaseModel):
    heart_rate: int = Field(..., gt=30, lt=200)
    blood_pressure: str
    temperature: float = Field(..., gt=90, lt=110)


class VitalSignsResponse(VitalSignsCreate):
    id: int
    patient_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


# ---------------------
# ACTIVITY
# ---------------------
class ActivityCreate(BaseModel):
    steps: int = Field(..., ge=0)
    calories_burned: float = Field(..., ge=0)


class ActivityResponse(ActivityCreate):
    id: int
    patient_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


# ---------------------
# ALERT
# ---------------------
class AlertCreate(BaseModel):
    patient_id: int
    type: str | None = None
    message: str
    severity: str | None = None


class AlertResponse(AlertCreate):
    id: int
    acknowledged: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------
# RISK ASSESSMENT
# ---------------------
class RiskAssessmentResponse(BaseModel):
    id: int
    patient_id: int
    risk_score: float
    risk_level: str
    factors: str
    recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True
