HealthTrack API Usage Guide
Base URL

http://127.0.0.1:8000

Authentication

Currently, this API supports no authentication.
If JWT/API keys are added in the future, include them like:

Header: Authorization: Bearer <token>

Endpoints
1. Create a Patient

POST /patients/

Request Body:
{
"name": "Alice",
"email": "alice@example.com
",
"age": 25
}

Response:
{
"name": "Alice",
"email": "alice@example.com
",
"age": 25
}

Errors:

422 Unprocessable Entity → invalid input
409 Conflict → email already exists (if implemented)
2. Get a Patient by ID

GET /patients/{patient_id}

Example Request:
GET /patients/1

Response:
{
"name": "Alice",
"email": "alice@example.com
",
"age": 25
}

Errors:

404 Not Found → patient does not exist
3. List All Patients

GET /patients/

Response:
[
{
"name": "Alice",
"email": "alice@example.com
",
"age": 25
},
{
"name": "Bob",
"email": "bob@example.com
",
"age": 30
}
]

4. Add Vital Signs for a Patient

POST /patients/{patient_id}/vitals

Request Body:
{
"heart_rate": 72,
"blood_pressure": "120/80",
"temperature": 98.6
}

Response:
{
"heart_rate": 72,
"blood_pressure": "120/80",
"temperature": 98.6
}

Errors:

404 Not Found → patient does not exist
422 Unprocessable Entity → invalid vitals data
5. Get Vital Signs for a Patient

GET /patients/{patient_id}/vitals

Response:
[
{
"heart_rate": 72,
"blood_pressure": "120/80",
"temperature": 98.6
},
{
"heart_rate": 68,
"blood_pressure": "118/78",
"temperature": 98.4
}
]

6. Add Activity Data for a Patient

POST /patients/{patient_id}/activities

Request Body:
{
"steps": 5000,
"calories_burned": 250.5
}

Response:
{
"steps": 5000,
"calories_burned": 250.5
}

Errors:

404 Not Found → patient does not exist
422 Unprocessable Entity → invalid activity data
7. Get Activity Data for a Patient

GET /patients/{patient_id}/activities

Response:
[
{
"steps": 5000,
"calories_burned": 250.5
},
{
"steps": 8000,
"calories_burned": 400
}
]

Notes
All endpoints return JSON.
Use Swagger UI at http://127.0.0.1:8000/docs
 for interactive testing.
Make sure the server is running: uvicorn main:app --reload
Error codes:
404 → resource not found
422 → invalid request body