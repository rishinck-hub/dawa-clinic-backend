from django.contrib import admin
from .models import Doctor, Patient, Medicine, Consultation, ConsultationMedicine

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Medicine)
admin.site.register(Consultation)
admin.site.register(ConsultationMedicine)
