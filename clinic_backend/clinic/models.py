from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    @property
    def patient_code(self):
        if self.id is None:
            return ""
        return f"PL00{self.id}"

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.dosage})"


class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()

    def __str__(self):
        return f"{self.patient.name} - {self.date.strftime('%Y-%m-%d')}"


class ConsultationMedicine(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    instructions = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.medicine.name}"


