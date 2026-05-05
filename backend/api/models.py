from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    room = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.specialty})"

class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class Queue(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='waiting')

    def __str__(self):
        return f"{self.patient.name} -> {self.doctor.name}"
