import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

conn_str = os.getenv("AZURE_SQL_CONNECTIONSTRING")

sql_commands = [
    """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Doctors')
    CREATE TABLE Doctors (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        specialty NVARCHAR(100),
        room NVARCHAR(10)
    )
    """,
    """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Patients')
    CREATE TABLE Patients (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        phone NVARCHAR(20),
        age INT
    )
    """,
    """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Queue')
    CREATE TABLE Queue (
        id INT IDENTITY(1,1) PRIMARY KEY,
        patient_id INT,
        doctor_id INT,
        time NVARCHAR(20),
        status NVARCHAR(20) DEFAULT 'waiting'
    )
    """
]

def setup_db():
    try:
        print("Connecting to Azure SQL...")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        for cmd in sql_commands:
            cursor.execute(cmd)
            print("Table created/verified.")
        
        conn.commit()
        conn.close()
        print("Database setup complete!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_db()
