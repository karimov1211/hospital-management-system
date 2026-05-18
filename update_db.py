import sqlite3

doctors = [
    "Abdullayev Bahriddin Bekturdi o'g'li",
    "Artiqova Malika G'ayrat qiz",
    "Bog'ibekov Oybek Bekpo'lat o'g'li",
    "Baxtiyarova Nafisa Murod qizi",
    "Boltabayeva Zuxra Hamidjon qizi",
    "Gulimova Sarvinoz Mansurbek qizi",
    "Jabbarova Shaydo Anvar qizi",
    "Janibekov Sherzod Farxod o'g'li"
]

patients = [
    "Komilova Nilufar Behzod qizi",
    "Kuryazova Laylo Bahodir qizi",
    "Nuraddinova Munira Dilshod qizi",
    "Ochilboyev Fayzulla Xayrulla o'g'li",
    "Ochilova Moxinur Xudayshukur qizi",
    "Olimboyeva Xolida Jamol qizi",
    "O'rinova O'g'iljon Umrbek qizi",
    "Qazaqova Gulruxsora Muzaffar qizi"
]

queue_patients = [
    "Raximova Mashxura Muzaffar qizi",
    "Romonberdiyev Farmon Diyor o'g'li",
    "Ro'ziboyeva Elnura Ergashbek qizi",
    "Ro'zimova Charosxon Ergash qizi",
    "Sa'dullayeva Oygul Muzaffar qizi",
    "Saparboyev Javoxir Shuxratjon o'g'li",
    "Sheripboyeva Gulmira Otabek qizi",
    "Tillayev Farruxbek Nodirbekovich"
]

def update_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT,
        room TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        age INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        time TEXT,
        status TEXT DEFAULT 'waiting'
    )
    ''')

    # Clear existing data
    cursor.execute("DELETE FROM Queue")
    cursor.execute("DELETE FROM Doctors")
    cursor.execute("DELETE FROM Patients")
    
    # Insert Doctors
    doctor_specialties = ["Kardiolog", "Terapevt", "Xirurg", "Nevropatolog", "LOR", "Stomatolog", "Oftalmolog", "Dermatolog"]
    for i, name in enumerate(doctors):
        cursor.execute("INSERT INTO Doctors (name, specialty, room) VALUES (?, ?, ?)", 
                       (name, doctor_specialties[i], str(100 + i + 1)))
        
    # Insert Patients
    for i, name in enumerate(patients):
        cursor.execute("INSERT INTO Patients (name, phone, age) VALUES (?, ?, ?)", 
                       (name, f"+998 90 000 {10 + i} 00", 25 + i))

    # Insert Queue Patients
    for i, name in enumerate(queue_patients):
        cursor.execute("INSERT INTO Patients (name, phone, age) VALUES (?, ?, ?)", 
                       (name, f"+998 90 111 {10 + i} 00", 30 + i))
    
    conn.commit()

    # Get the inserted doctors and patients to create queue entries
    cursor.execute("SELECT id FROM Doctors")
    doc_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM Patients")
    all_patients = cursor.fetchall()
    
    # Create queue entries for the last 8 patients
    queue_pats = all_patients[-8:]
    for i, p in enumerate(queue_pats):
        doc_id = doc_ids[i % len(doc_ids)]
        time_str = f"{10 + i}:00"
        cursor.execute("INSERT INTO Queue (patient_id, doctor_id, time, status) VALUES (?, ?, ?, ?)",
                       (p[0], doc_id, time_str, "kutilmoqda"))

    conn.commit()
    conn.close()
    print("Database updated successfully with SQLite!")

if __name__ == '__main__':
    update_db()
