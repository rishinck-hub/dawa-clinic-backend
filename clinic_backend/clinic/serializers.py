from rest_framework import serializers
from django.db import IntegrityError
from .models import Doctor, Medicine
from accounts.models import User
from .models import Patient, Consultation, ConsultationMedicine, Medicine



class DoctorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialization', 'phone', 'email',
            'username', 'password'
        ]

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        if not username or not password:
            raise serializers.ValidationError("Username and password are required for creating a doctor")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Username already exists"})

        user = User.objects.create_user(
            username=username,
            email=validated_data.get('email'),
            password=password,
            role='DOCTOR'
        )

        try:
            doctor, created = Doctor.objects.get_or_create(
                user=user,
                defaults=validated_data
            )
            if not created:
                for key, value in validated_data.items():
                    setattr(doctor, key, value)
                doctor.save()
        except IntegrityError:
            user.delete()
            raise serializers.ValidationError(
                {"detail": "Doctor profile already exists for this user"}
            )
        return doctor

    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        instance.name = validated_data.get('name', instance.name)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if password:
            instance.user.set_password(password)
            instance.user.save()

        return instance


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    patient_code = serializers.CharField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'patient_code',
            'name',
            'phone',
            'age',
            'gender',
            'address',
            'created_by',
        ]
        read_only_fields = ['created_by']


class ConsultationMedicineSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = ConsultationMedicine
        fields = ['medicine_name', 'instructions']


class ConsultationSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        write_only=True
    )
    medicines = ConsultationMedicineSerializer(
        source='consultationmedicine_set',
        many=True,
        read_only=True
    )
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_code = serializers.CharField(source='patient.patient_code', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id',
            'patient',
            'patient_name',
            'patient_code',
            'notes',
            'date',
            'medicines',
        ]



