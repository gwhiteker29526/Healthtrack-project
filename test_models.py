import pytest
from sqlalchemy.orm import Session
from database import SessionLocal
import models

@pytest.fixture
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_patient_creation(db_session: Session):
    patient = models.Patient(name="Alice", email="alice@example.com", age=25)
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    assert patient.id is not None
    assert patient.name == "Alice"