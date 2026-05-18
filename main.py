from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os

app = FastAPI(title="MedCare API")

# Mount frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

DB_PATH = "hospital.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT,
        room TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        age INTEGER
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        time TEXT,
        status TEXT DEFAULT 'waiting'
    )''')
    conn.commit()
    conn.close()

init_db()

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

class QueueCreate(BaseModel):
    patient: int
    doctor: int
    time: str
    status: str = "waiting"

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

# --- Doctor Endpoints ---
@app.get("/api/doctors/")
def get_doctors():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty, room FROM Doctors")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r["id"], "name": r["name"], "specialty": r["specialty"], "room": r["room"]} for r in rows]

@app.post("/api/doctors/")
def add_doctor(doctor: Doctor):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Doctors (name, specialty, room) VALUES (?, ?, ?)",
                   (doctor.name, doctor.specialty, doctor.room))
    conn.commit()
    conn.close()
    return {"status": "Doctor added"}

@app.delete("/api/doctors/{doctor_id}/")
def delete_doctor(doctor_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    conn.close()
    return {"status": "Doctor deleted"}

# --- Patient Endpoints ---
@app.get("/api/patients/")
def get_patients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, age FROM Patients")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r["id"], "name": r["name"], "phone": r["phone"], "age": r["age"]} for r in rows]

@app.post("/api/patients/")
def add_patient(patient: Patient):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Patients (name, phone, age) VALUES (?, ?, ?)",
                   (patient.name, patient.phone, patient.age))
    conn.commit()
    conn.close()
    return {"status": "Patient added"}

@app.delete("/api/patients/{patient_id}/")
def delete_patient(patient_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()
    return {"status": "Patient deleted"}

# --- Queue Endpoints ---
@app.get("/api/queue/")
def get_queue():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.id, q.patient_id, q.doctor_id, q.time, q.status,
               p.name as patient_name, d.name as doctor_name
        FROM Queue q
        LEFT JOIN Patients p ON q.patient_id = p.id
        LEFT JOIN Doctors d ON q.doctor_id = d.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{
        "id": r["id"],
        "patient_id": r["patient_id"],
        "doctor_id": r["doctor_id"],
        "time": r["time"],
        "status": r["status"],
        "patient_name": r["patient_name"],
        "doctor_name": r["doctor_name"]
    } for r in rows]

@app.post("/api/queue/")
def add_to_queue(item: QueueCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Queue (patient_id, doctor_id, time, status) VALUES (?, ?, ?, ?)",
                   (item.patient, item.doctor, item.time, item.status))
    conn.commit()
    conn.close()
    return {"status": "Added to queue"}

@app.delete("/api/queue/{queue_id}/")
def delete_queue(queue_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Queue WHERE id = ?", (queue_id,))
    conn.commit()
    conn.close()
    return {"status": "Queue item deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
