# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine

# -----------------------------
# Initialize FastAPI app
# -----------------------------
app = FastAPI(title="HealthTrack API")

# -----------------------------
# Create tables (if not using Alembic migrations)
# -----------------------------
models.Base.metadata.create_all(bind=engine)

# -----------------------------
# Dependency: DB session
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Patients Endpoints
# -----------------------------
@app.post("/patients/", response_model=schemas.PatientCreate)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@app.get("/patients/{patient_id}", response_model=schemas.PatientCreate)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/patients/", response_model=list[schemas.PatientCreate])
def read_all_patients(db: Session = Depends(get_db)):
    return crud.get_all_patients(db)

# -----------------------------
# Vital Signs Endpoints
# -----------------------------
@app.post("/patients/{patient_id}/vitals", response_model=schemas.VitalSignsCreate)
def add_vitals(patient_id: int, vitals: schemas.VitalSignsCreate, db: Session = Depends(get_db)):
    return crud.add_vitals(db, patient_id, vitals)

@app.get("/patients/{patient_id}/vitals", response_model=list[schemas.VitalSignsCreate])
def get_vitals(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_vitals(db, patient_id)

# -----------------------------
# Activity Tracking Endpoints
# -----------------------------
@app.post("/patients/{patient_id}/activities", response_model=schemas.ActivityCreate)
def add_activity(patient_id: int, activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return crud.add_activity(db, patient_id, activity)

@app.get("/patients/{patient_id}/activities", response_model=list[schemas.ActivityCreate])
def get_activities(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_activities(db, patient_id)

# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the HealthTrack API"}