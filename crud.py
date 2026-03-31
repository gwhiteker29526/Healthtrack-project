from sqlalchemy.orm import Session
import models

# Patient CRUD
def create_patient(db: Session, patient):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)
    if patient:
        db.delete(patient)
        db.commit()
    return patient


# Vital Signs
def add_vitals(db: Session, patient_id: int, vitals):
    record = models.VitalSigns(patient_id=patient_id, **vitals.dict())
    db.add(record)
    db.commit()
    return record


# Activity Data
def add_activity(db: Session, patient_id: int, activity):
    record = models.ActivityData(patient_id=patient_id, **activity.dict())
    db.add(record)
    db.commit()
    return record


# Filtering example
def get_vitals_by_date(db, patient_id, start, end):
    return db.query(models.VitalSigns).filter(
        models.VitalSigns.patient_id == patient_id,
        models.VitalSigns.recorded_at.between(start, end)
    ).all()