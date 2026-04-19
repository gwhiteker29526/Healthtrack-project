# HealthTrack System Setup

## 1. Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic dash plotly pandas

## 2. Run API
uvicorn main:app --reload

## 3. Run Dashboard
python dashboard.py

## 4. Access
API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs
Dashboard: http://127.0.0.1:8050
