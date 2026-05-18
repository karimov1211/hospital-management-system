from django.db import transaction
from api.models import Doctor, Patient, Queue

def seed_database():
    try:
        print("Auto-seeding using ORM started...")
        with transaction.atomic():
            # Clear old records first
            Queue.objects.all().delete()
            Doctor.objects.all().delete()
            Patient.objects.all().delete()
            
            # 8 Doctors (from the image list, items 1-8)
            doctors_data = [
                {"name": "Abdullayev Bahriddin Bekturdi o'g'li", "specialty": "Kardiolog", "room": "101"},
                {"name": "Artiqova Malika G'ayrat qiz", "specialty": "Terapevt", "room": "102"},
                {"name": "Bog'ibekov Oybek Bekpo'lat o'g'li", "specialty": "Xirurg", "room": "103"},
                {"name": "Baxtiyarova Nafisa Murod qizi", "specialty": "Nevropatolog", "room": "104"},
                {"name": "Boltabayeva Zuxra Hamidjon qizi", "specialty": "LOR", "room": "105"},
                {"name": "Gulimova Sarvinoz Mansurbek qiz1", "specialty": "Stomatolog", "room": "106"},
                {"name": "Jabbarova Shaydo Anvar qizi", "specialty": "Oftalmolog", "room": "107"},
                {"name": "Janibekov Sherzod Farxod o'g'li", "specialty": "Dermatolog", "room": "108"}
            ]
            doctors = []
            for doc_data in doctors_data:
                doc = Doctor.objects.create(**doc_data)
                doctors.append(doc)
            
            # 16 Patients (from the image list, items 9-24)
            patients_data = [
                {"name": "Komilova Nilufar Behzod qizi", "phone": "+998 90 000 10 00", "age": 25},
                {"name": "Kuryazova Laylo Bahodir qizi", "phone": "+998 90 000 11 00", "age": 26},
                {"name": "Nuraddinova Munira Dilshod qizi", "phone": "+998 90 000 12 00", "age": 27},
                {"name": "Ochilboyev Fayzulla Xayrulla o'g'li", "phone": "+998 90 000 13 00", "age": 28},
                {"name": "Ochilova Moxinur Xudayshukur qizi", "phone": "+998 90 000 14 00", "age": 29},
                {"name": "Olimboyeva Xolida Jamol qizi", "phone": "+998 90 000 15 00", "age": 30},
                {"name": "O'rinova O'g'iljon Umrbek qizi", "phone": "+998 90 000 16 00", "age": 31},
                {"name": "Qazaqova Gulruxsora Muzaffar qizi", "phone": "+998 90 000 17 00", "age": 32},
                
                {"name": "Raximova Mashxura Muzaffar qizi", "phone": "+998 90 111 10 00", "age": 33},
                {"name": "Romonberdiyev Farmon Diyor o'g'li", "phone": "+998 90 111 11 00", "age": 34},
                {"name": "Ro'ziboyeva Elnura Ergashbek qizi", "phone": "+998 90 111 12 00", "age": 35},
                {"name": "Ro'zimova Charosxon Ergash qizi", "phone": "+998 90 111 13 00", "age": 36},
                {"name": "Sa'dullayeva Oygul Muzaffar qizi", "phone": "+998 90 111 14 00", "age": 37},
                {"name": "Saparboyev Javoxir Shuxratjon o'g'li", "phone": "+998 90 111 15 00", "age": 38},
                {"name": "Sheripboyeva Gulmira Otabek qizi", "phone": "+998 90 111 16 00", "age": 39},
                {"name": "Tillayev Farruxbek Nodirbekovich", "phone": "+998 90 111 17 00", "age": 40}
            ]
            patients = []
            for pat_data in patients_data:
                pat = Patient.objects.create(**pat_data)
                patients.append(pat)
            
            # Queues (8 items mapping patient 9-16 to doctor 1-8)
            queue_times = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30"]
            for idx in range(8):
                pat = patients[idx + 8] # Patient 9 to 16
                doc = doctors[idx]      # Doctor 1 to 8
                Queue.objects.create(
                    patient=pat,
                    doctor=doc,
                    time=queue_times[idx],
                    status="kutilmoqda"
                )
            print("Database successfully seeded using ORM!")
            return True
    except Exception as e:
        print(f"Auto-seeding error using ORM: {e}")
        return False
