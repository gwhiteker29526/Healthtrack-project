
CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(120) UNIQUE,
  password_hash VARCHAR(255),
  role VARCHAR(20)
);

CREATE TABLE patients (
  patient_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  date_of_birth DATE,
  blood_type VARCHAR(5)
);

CREATE TABLE devices (
  device_id SERIAL PRIMARY KEY,
  patient_id INT REFERENCES patients(patient_id),
  device_type VARCHAR(50)
);

CREATE TABLE readings (
  reading_id SERIAL PRIMARY KEY,
  patient_id INT REFERENCES patients(patient_id),
  reading_type VARCHAR(50),
  reading_value DECIMAL,
  reading_time TIMESTAMP
);

CREATE TABLE alerts (
  alert_id SERIAL PRIMARY KEY,
  patient_id INT REFERENCES patients(patient_id),
  severity VARCHAR(20),
  message TEXT
);

CREATE TABLE appointments (
  appointment_id SERIAL PRIMARY KEY,
  patient_id INT REFERENCES patients(patient_id),
  provider_name VARCHAR(100),
  appointment_time TIMESTAMP
);
