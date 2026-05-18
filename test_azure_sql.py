import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.environ.get(
    'AZURE_SQL_CONNECTIONSTRING',
    'Driver={ODBC Driver 17 for SQL Server};Server=tcp:azurefreetrial.database.windows.net,1433;Database=azurefreetutorial;Uid=azure-admin;Pwd=Hamdambek2006;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
)

print(f"Testing connection with connection string:")
# Hide password in print
print(connection_string.replace('Hamdambek2006', '******'))

try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print("Query successful! Server version:")
    print(row[0])
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
