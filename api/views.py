from rest_framework import viewsets
from .models import Doctor, Patient, Queue
from .serializers import DoctorSerializer, PatientSerializer, QueueSerializer
from .seeder import seed_database

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        if Doctor.objects.count() == 0:
            seed_database()
        return Doctor.objects.all()

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        if Doctor.objects.count() == 0:
            seed_database()
        return Patient.objects.all()

class QueueViewSet(viewsets.ModelViewSet):
    serializer_class = QueueSerializer

    def get_queryset(self):
        if Doctor.objects.count() == 0:
            seed_database()
        return Queue.objects.all()

