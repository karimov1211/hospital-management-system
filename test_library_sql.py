import pyodbc
import os

connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:library-server-karimov1211.database.windows.net,1433;"
    "Database=LibraryDB;"
    "Uid=dbadmin;"
    "Pwd=AzurePassword123!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

print(f"Testing library DB connection...")
try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM sysobjects")
    row = cursor.fetchone()
    print("Query successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
