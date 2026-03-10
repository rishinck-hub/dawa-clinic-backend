from django.urls import path
from .views import (
    DoctorListCreateView,
    DoctorDetailView,
    MedicineListCreateView,
    MedicineDetailView,
    PatientListCreateView,
    PatientDetailView,
    ConsultationCreateView,
    ConsultationHistoryView,
    AdminStatsView
)


urlpatterns = [
    path('admin/doctors/', DoctorListCreateView.as_view()),
    path('admin/doctors/<int:pk>/', DoctorDetailView.as_view()),
    path('admin/medicines/', MedicineListCreateView.as_view()),
    path('admin/medicines/<int:pk>/', MedicineDetailView.as_view()),
    path('doctor/patients/', PatientListCreateView.as_view()),
    path('doctor/patients/<int:pk>/', PatientDetailView.as_view()),
    path('doctor/consultations/', ConsultationCreateView.as_view()),
    path('doctor/consultations/history/', ConsultationHistoryView.as_view()),
    path('admin/stats/', AdminStatsView.as_view()),

]
