from django.contrib import admin
from .models import Doctor, Patient, Queue

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'room')
    search_fields = ('name', 'specialty')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'age')
    search_fields = ('name', 'phone')

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'time', 'status')
    list_filter = ('status', 'doctor')
