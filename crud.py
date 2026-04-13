from sqlalchemy.orm import Session
import models
from models import Patient, VitalSigns, ActivityData, RiskAssessment, Alert
from risk import calculate_risk

# -----------------------------
# PATIENT CRUD (OPTIMIZED)
# -----------------------------
def create_patient(db: Session, patient):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_all_patients(db: Session, limit: int = 50):
    return db.query(Patient).limit(limit).all()

def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)
    if patient:
        db.delete(patient)
        db.commit()
    return patient


# -----------------------------
# VITAL SIGNS (OPTIMIZED)
# -----------------------------
def add_vitals(db: Session, patient_id: int, vitals):
    record = VitalSigns(patient_id=patient_id, **vitals.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_vitals(db: Session, patient_id: int, limit: int = 50):
    return db.query(VitalSigns)\
        .filter(VitalSigns.patient_id == patient_id)\
        .order_by(VitalSigns.recorded_at.desc())\
        .limit(limit)\
        .all()

def get_vitals_by_date(db: Session, patient_id: int, start, end):
    return db.query(VitalSigns)\
        .filter(
            VitalSigns.patient_id == patient_id,
            VitalSigns.recorded_at.between(start, end)
        ).all()


# -----------------------------
# ACTIVITY DATA (OPTIMIZED)
# -----------------------------
def add_activity(db: Session, patient_id: int, activity):
    record = ActivityData(patient_id=patient_id, **activity.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_activities(db: Session, patient_id: int, limit: int = 50):
    return db.query(ActivityData)\
        .filter(ActivityData.patient_id == patient_id)\
        .order_by(ActivityData.recorded_at.desc())\
        .limit(limit)\
        .all()


# -----------------------------
# ALERTS (CLEANED + OPTIMIZED)
# -----------------------------
def create_alert(db: Session, patient_id: int, message: str, severity: str, type: str = "vital"):
    alert = Alert(
        patient_id=patient_id,
        message=message,
        severity=severity,
        type=type
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def get_alert(db: Session, alert_id: int):
    return db.query(Alert).filter(Alert.id == alert_id).first()

def get_all_alerts(db: Session, limit: int = 100):
    return db.query(Alert)\
        .order_by(Alert.created_at.desc())\
        .limit(limit)\
        .all()

def acknowledge_alert(db: Session, alert_id: int):
    alert = get_alert(db, alert_id)
    if alert:
        alert.acknowledged = True
        db.commit()
    return alert


# -----------------------------
# RISK (OPTIMIZED)
# -----------------------------
def create_risk_assessment(db: Session, patient_id: int, vitals, activities):
    score, level, factors, recommendation = calculate_risk(vitals, activities)

    risk = RiskAssessment(
        patient_id=patient_id,
        risk_score=score,
        risk_level=level,
        factors=", ".join(factors),  # cleaner storage
        recommendation=recommendation
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk

def get_risks_for_patient(db: Session, patient_id: int):
    return db.query(RiskAssessment)\
        .filter(RiskAssessment.patient_id == patient_id)\
        .order_by(RiskAssessment.created_at.desc())\
        .all()
