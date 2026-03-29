from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsAdmin, IsDoctor, IsAdminOrReadOnly
from .models import Doctor, Medicine, Patient, Consultation, ConsultationMedicine
from .serializers import DoctorSerializer, MedicineSerializer, PatientSerializer, ConsultationSerializer


def _extract_patient_id(search_query):
    if not search_query:
        return None
    query = search_query.strip().upper()
    if query.startswith("PL00"):
        code_part = query[4:]
        if code_part.isdigit():
            return int(code_part)
    if query.isdigit():
        return int(query)
    return None


class SecureTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "JWT working!"})
    


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Admin access granted"})


class DoctorListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        doctors = Doctor.objects.all()
        
        # Search by name or phone
        search_query = request.GET.get('search', '').strip()
        if search_query:
            from django.db.models import Q
            doctors = doctors.filter(
                Q(name__icontains=search_query) | Q(phone__icontains=search_query)
            )
        
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

    def put(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

    def delete(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            doctor.user.delete()
            doctor.delete()
            return Response({"message": "Doctor deleted"}, status=204)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)


class MedicineListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        medicines = Medicine.objects.all()
        
        # Search by name or ID
        search_query = request.GET.get('search', '').strip()
        if search_query:
            from django.db.models import Q
            medicines = medicines.filter(
                Q(name__icontains=search_query) | Q(id__icontains=search_query)
            )
        
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MedicineDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            medicine = Medicine.objects.get(pk=pk)
            serializer = MedicineSerializer(medicine)
            return Response(serializer.data)
        except Medicine.DoesNotExist:
            return Response({"error": "Medicine not found"}, status=404)

    def put(self, request, pk):
        try:
            medicine = Medicine.objects.get(pk=pk)
            serializer = MedicineSerializer(medicine, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Medicine.DoesNotExist:
            return Response({"error": "Medicine not found"}, status=404)

    def delete(self, request, pk):
        try:
            medicine = Medicine.objects.get(pk=pk)
            medicine.delete()
            return Response({"message": "Medicine deleted"}, status=204)
        except Medicine.DoesNotExist:
            return Response({"error": "Medicine not found"}, status=404)

class PatientListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor profile not found. Please contact administrator."}, status=400)
        
        patients = Patient.objects.filter(created_by=doctor)
        
        # Search by name, phone, ID, or patient code (PL00<id>)
        search_query = request.GET.get('search', '').strip()
        if search_query:
            from django.db.models import Q
            search_q = Q(name__icontains=search_query) | Q(phone__icontains=search_query)
            patient_id = _extract_patient_id(search_query)
            if patient_id is not None:
                search_q = search_q | Q(id=patient_id)
            patients = patients.filter(search_q)
        
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            # Create a default doctor profile if it doesn't exist
            doctor = Doctor.objects.create(
                user=request.user,
                name=request.user.username,
                specialization='General',
                phone='',
                email=''
            )
        
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=doctor)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(user=request.user)
            patient = Patient.objects.get(pk=pk, created_by=doctor)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor profile not found"}, status=400)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)

    def put(self, request, pk):
        try:
            doctor = Doctor.objects.get(user=request.user)
            patient = Patient.objects.get(pk=pk, created_by=doctor)
            serializer = PatientSerializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor profile not found"}, status=400)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)

    def delete(self, request, pk):
        try:
            doctor = Doctor.objects.get(user=request.user)
            patient = Patient.objects.get(pk=pk, created_by=doctor)
            patient.delete()
            return Response({"message": "Patient deleted"}, status=204)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor profile not found"}, status=400)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)

class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        total_doctors = Doctor.objects.count()
        total_medicines = Medicine.objects.count()
        total_patients = Patient.objects.count()
        return Response({
            "total_doctors": total_doctors,
            "total_medicines": total_medicines,
            "total_patients": total_patients,
        })


class ConsultationCreateView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            doctor = Doctor.objects.create(
                user=request.user,
                name=request.user.username,
                specialization='General',
                phone='',
                email=''
            )

        data = request.data.copy()
        medicines_data = data.pop('medicines', [])

        serializer = ConsultationSerializer(data=data)
        if serializer.is_valid():
            patient = serializer.validated_data['patient']
            if patient.created_by_id != doctor.id:
                return Response(
                    {"detail": "Patient does not belong to this doctor."},
                    status=400
                )

            consultation = serializer.save(doctor=doctor)

            for item in medicines_data or []:
                medicine_id = item.get('medicine_id')
                if not medicine_id:
                    continue
                try:
                    medicine = Medicine.objects.get(pk=medicine_id)
                except Medicine.DoesNotExist:
                    return Response(
                        {"detail": f"Medicine {medicine_id} not found."},
                        status=400
                    )
                ConsultationMedicine.objects.create(
                    consultation=consultation,
                    medicine=medicine,
                    instructions=item.get('instructions', '')
                )

            return Response(
                ConsultationSerializer(consultation).data,
                status=201
            )
        return Response(serializer.errors, status=400)


class ConsultationHistoryView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response([])
        
        query = request.GET.get('search', '')
        from django.db.models import Q
        search_q = Q(created_by=doctor)
        if query:
            patient_id = _extract_patient_id(query)
            patient_filter = Q(name__icontains=query) | Q(phone__icontains=query)
            if patient_id is not None:
                patient_filter = patient_filter | Q(id=patient_id)
            search_q = search_q & patient_filter

        patients = Patient.objects.filter(search_q)

        consultations = Consultation.objects.filter(patient__in=patients)
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)


class PatientConsultationHistoryView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor profile not found"}, status=400)

        try:
            patient = Patient.objects.get(pk=pk, created_by=doctor)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)

        consultations = Consultation.objects.filter(patient=patient).order_by('-date')
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)
