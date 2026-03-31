from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    vital_signs = relationship("VitalSigns", back_populates="patient", cascade="all, delete")
    activities = relationship("ActivityData", back_populates="patient", cascade="all, delete")


class VitalSigns(Base):
    __tablename__ = "vital_signs"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    heart_rate = Column(Integer, nullable=False)
    blood_pressure = Column(String(20))
    temperature = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="vital_signs")


class ActivityData(Base):
    __tablename__ = "activity_data"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    steps = Column(Integer, default=0)
    calories_burned = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="activities")