from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MedCare API")

# Database connection configuration
# Azure SQL uchun Connection String .env faylida bo'lishi kerak
DB_CONFIG = os.getenv("AZURE_SQL_CONNECTIONSTRING")

def get_db_connection():
    try:
        conn = pyodbc.connect(DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Models
class Doctor(BaseModel):
    id: Optional[int] = None
    name: str
    specialty: str
    room: str

class Patient(BaseModel):
    id: Optional[int] = None
    name: str
    phone: str
    age: int

class QueueItem(BaseModel):
    id: Optional[int] = None
    patient_id: int
    doctor_id: int
    time: str
    status: str

@app.get("/")
def read_root():
    return {"message": "MedCare Hospital Management API is running"}

# --- Doctor Endpoints ---
@app.get("/doctors", response_model=List[Doctor])
def get_doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty, room FROM Doctors")
    rows = cursor.fetchall()
    doctors = [{"id": r[0], "name": r[1], "specialty": r[2], "room": r[3]} for r in rows]
    conn.close()
    return doctors

@app.post("/doctors")
def add_doctor(doctor: Doctor):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Doctors (name, specialty, room) VALUES (?, ?, ?)", 
                   (doctor.name, doctor.specialty, doctor.room))
    conn.commit()
    conn.close()
    return {"status": "Doctor added"}

# --- Patient Endpoints ---
@app.get("/patients", response_model=List[Patient])
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, age FROM Patients")
    rows = cursor.fetchall()
    patients = [{"id": r[0], "name": r[1], "phone": r[2], "age": r[3]} for r in rows]
    conn.close()
    return patients

@app.post("/patients")
def add_patient(patient: Patient):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Patients (name, phone, age) VALUES (?, ?, ?)", 
                   (patient.name, patient.phone, patient.age))
    conn.commit()
    conn.close()
    return {"status": "Patient added"}

# --- Queue Endpoints ---
@app.get("/queue", response_model=List[QueueItem])
def get_queue():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, patient_id, doctor_id, time, status FROM Queue")
    rows = cursor.fetchall()
    queue = [{"id": r[0], "patient_id": r[1], "doctor_id": r[2], "time": r[3], "status": r[4]} for r in rows]
    conn.close()
    return queue

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
