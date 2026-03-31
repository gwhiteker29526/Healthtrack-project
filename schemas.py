from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    age: int = Field(..., gt=0, lt=120)


class VitalSignsCreate(BaseModel):
    heart_rate: int = Field(..., gt=30, lt=200)
    blood_pressure: str
    temperature: float = Field(..., gt=90, lt=110)


class ActivityCreate(BaseModel):
    steps: int = Field(..., ge=0)
    calories_burned: float = Field(..., ge=0)