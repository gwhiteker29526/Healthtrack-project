from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from risk import calculate_risk
from crud import create_risk_assessment, get_risks_for_patient
import models
import schemas
import crud
from database import SessionLocal, engine
from alerts import check_vitals, check_activity
from notifications import send_notification

# -----------------------------
# Initialize FastAPI app
# -----------------------------
app = FastAPI(
    title="HealthTrack API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

models.Base.metadata.create_all(bind=engine)

# -----------------------------
# SIMPLE CACHE (optimization)
# -----------------------------
cache = {}

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
# Patients Endpoints (OPTIMIZED)
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

@app.get("/patients/", response_model=List[schemas.PatientCreate])
def read_all_patients(limit: int = Query(50, le=100), db: Session = Depends(get_db)):
    return crud.get_all_patients(db, limit)

# -----------------------------
# Vital Signs (OPTIMIZED)
# -----------------------------
@app.post("/patients/{patient_id}/vitals", response_model=schemas.VitalSignsCreate)
def add_vitals(patient_id: int, vitals: schemas.VitalSignsCreate, db: Session = Depends(get_db)):
    new_vitals = crud.add_vitals(db, patient_id, vitals)

    alerts = check_vitals(new_vitals)

    for message, severity in alerts:
        alert = crud.create_alert(db, new_vitals.patient_id, message, severity)
        send_notification(alert)

    cache.pop("alerts", None)  # clear cache if new data added
    return new_vitals

@app.get("/patients/{patient_id}/vitals", response_model=List[schemas.VitalSignsCreate])
def get_vitals(
    patient_id: int,
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_vitals(db, patient_id, limit)

# -----------------------------
# Activity Tracking (OPTIMIZED)
# -----------------------------
@app.post("/patients/{patient_id}/activities", response_model=schemas.ActivityCreate)
def add_activity(patient_id: int, activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    new_activity = crud.add_activity(db, patient_id, activity)

    alerts = check_activity(new_activity)

    for message, severity in alerts:
        alert = crud.create_alert(db, new_activity.patient_id, message, severity)
        send_notification(alert)

    cache.pop("alerts", None)
    return new_activity

@app.get("/patients/{patient_id}/activities", response_model=List[schemas.ActivityCreate])
def get_activities(
    patient_id: int,
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_activities(db, patient_id, limit)

# -----------------------------
# Alerts (WITH CACHING)
# -----------------------------
@app.get("/alerts/", response_model=List[schemas.AlertCreate])
def get_alerts(db: Session = Depends(get_db)):
    if "alerts" in cache:
        return cache["alerts"]

    alerts = crud.get_all_alerts(db)
    cache["alerts"] = alerts
    return alerts

@app.put("/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = crud.acknowledge_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    cache.pop("alerts", None)  # invalidate cache
    return {"status": "Alert acknowledged", "alert_id": alert.id}

# -----------------------------
# Risk (OPTIMIZED)
# -----------------------------
@app.post("/patients/{patient_id}/risk")
def assess_risk(patient_id: int, db: Session = Depends(get_db)):
    vitals_list = crud.get_vitals(db, patient_id, limit=1)
    activities_list = crud.get_activities(db, patient_id, limit=1)

    if not vitals_list or not activities_list:
        raise HTTPException(status_code=400, detail="Insufficient data for risk assessment")

    latest_vitals = vitals_list[0]
    latest_activity = activities_list[0]

    risk = create_risk_assessment(db, patient_id, latest_vitals, latest_activity)

    return {
        "patient_id": patient_id,
        "risk_score": risk.risk_score,
        "risk_level": risk.risk_level,
        "factors": risk.factors,
        "recommendation": risk.recommendation
    }

@app.get("/patients/{patient_id}/risk")
def get_risk_history(patient_id: int, db: Session = Depends(get_db)):
    risks = get_risks_for_patient(db, patient_id)

    return [
        {
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "factors": r.factors,
            "recommendation": r.recommendation,
            "date": r.created_at
        } for r in risks
    ]

# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the HealthTrack API"}
