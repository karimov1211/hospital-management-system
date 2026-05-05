# MedCare - Kasalxona Boshqaruv Tizimi

Ushbu loyiha shifokorlar va bemorlar navbatini boshqarish uchun mo'ljallangan zamonaviy Full-stack Web-ilovadir.

## Loyiha tarkibi
- **Frontend:** HTML, CSS, JavaScript (Lucide icons bilan).
- **Backend:** Python FastAPI.
- **Ma'lumotlar bazasi:** Azure SQL Database.

## O'rnatish va ishga tushirish

### 1. Backendni sozlash
1. `backend` papkasiga kiring.
2. Kerakli kutubxonalarni o'rnating: `pip install -r requirements.txt`.
3. `.env` fayliga Azure SQL ulanish manzilingizni yozing.
4. Serverni ishga tushiring: `python main.py`.

### 2. Azure SQL sozlamalari
Azure-da baza yaratgandan so'ng, quyidagi jadvallarni yarating:
```sql
CREATE TABLE Doctors (id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(100), specialty NVARCHAR(100), room NVARCHAR(10));
CREATE TABLE Patients (id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(100), phone NVARCHAR(20), age INT);
CREATE TABLE Queue (id INT IDENTITY(1,1) PRIMARY KEY, patient_id INT, doctor_id INT, time NVARCHAR(20), status NVARCHAR(20));
```

## GitHub-ga yuklash
Loyiha allaqachon GitHub-ga yuklangan: [https://github.com/karimov1211/hospital-management-system](https://github.com/karimov1211/hospital-management-system)
