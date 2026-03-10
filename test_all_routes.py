#!/usr/bin/env python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# First, login to get a token
print("=" * 60)
print("TESTING ALL API ROUTES")
print("=" * 60)

print("\n1. Testing LOGIN (POST /api/login/)")
login_response = requests.post(f"{BASE_URL}/login/", json={"username": "admin", "password": "admin123"})
print(f"   Status: {login_response.status_code}")
if login_response.status_code == 200:
    token_data = login_response.json()
    print(f"   ✓ Login successful")
    print(f"   - Role: {token_data.get('role')}")
    token = token_data.get('access')
else:
    print(f"   ✗ Login failed: {login_response.text}")
    token = None

# Set up headers with token
headers = {"Authorization": f"Bearer {token}"} if token else {}

print("\n" + "=" * 60)
print("ADMIN ROUTES (requires ADMIN token)")
print("=" * 60)

# 2. Doctor routes
print("\n2. Testing GET /api/admin/doctors/")
response = requests.get(f"{BASE_URL}/admin/doctors/", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✓ Doctors list retrieved")
    print(f"   - Count: {len(response.json())} doctors")
else:
    print(f"   ✗ Failed: {response.text[:100]}")

print("\n3. Testing POST /api/admin/doctors/ (Create doctor)")
doctor_data = {
    "name": "Dr. John Doe",
    "specialization": "General Practitioner",
    "phone": "555-1234",
    "email": "john@clinic.com",
    "username": "dr_john",
    "password": "password123"
}
response = requests.post(f"{BASE_URL}/admin/doctors/", json=doctor_data, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 201:
    print(f"   ✓ Doctor created successfully")
elif response.status_code == 400:
    print(f"   ! Doctor might already exist (400 error)")
else:
    print(f"   ✗ Failed: {response.text[:100]}")

# 4. Medicines routes
print("\n4. Testing GET /api/admin/medicines/")
response = requests.get(f"{BASE_URL}/admin/medicines/", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✓ Medicines list retrieved")
    print(f"   - Count: {len(response.json())} medicines")
else:
    print(f"   ✗ Failed: {response.text[:100]}")

print("\n5. Testing POST /api/admin/medicines/ (Create medicine)")
medicine_data = {
    "name": "Paracetamol",
    "dosage": "500mg"
}
response = requests.post(f"{BASE_URL}/admin/medicines/", json=medicine_data, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 201:
    print(f"   ✓ Medicine created successfully")
elif response.status_code == 400:
    print(f"   ! Medicine might already exist (400 error)")
else:
    print(f"   ✗ Failed: {response.text[:100]}")

print("\n" + "=" * 60)
print("DOCTOR ROUTES (requires DOCTOR token)")
print("=" * 60)

# Get doctor token
print("\nLogging in as doctor...")
doctor_login = requests.post(f"{BASE_URL}/login/", json={"username": "doctor", "password": "doctor123"})
if doctor_login.status_code == 200:
    doctor_token = doctor_login.json().get('access')
    doctor_headers = {"Authorization": f"Bearer {doctor_token}"}
    print("✓ Doctor login successful")
else:
    print(f"✗ Doctor login failed")
    doctor_headers = {}

# 6. Patients routes
print("\n6. Testing GET /api/doctor/patients/")
response = requests.get(f"{BASE_URL}/doctor/patients/", headers=doctor_headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✓ Patients list retrieved")
    print(f"   - Count: {len(response.json())} patients")
else:
    print(f"   ✗ Failed: {response.text[:100]}")

print("\n7. Testing POST /api/doctor/patients/ (Create patient)")
patient_data = {
    "name": "John Smith",
    "phone": "555-5678",
    "age": 35,
    "gender": "Male",
    "address": "123 Main St"
}
response = requests.post(f"{BASE_URL}/doctor/patients/", json=patient_data, headers=doctor_headers)
print(f"   Status: {response.status_code}")
if response.status_code == 201:
    print(f"   ✓ Patient created successfully")
    patient_id = response.json().get('id')
elif response.status_code == 400:
    print(f"   ! Patient might already exist (400 error)")
    patient_id = None
else:
    print(f"   ✗ Failed: {response.text[:100]}")
    patient_id = None

# 8. Consultations routes
print("\n8. Testing GET /api/doctor/consultations/history/")
response = requests.get(f"{BASE_URL}/doctor/consultations/history/", headers=doctor_headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✓ Consultation history retrieved")
    print(f"   - Count: {len(response.json())} consultations")
else:
    print(f"   ✗ Failed: {response.text[:100]}")

print("\n9. Testing POST /api/doctor/consultations/ (Create consultation)")
if patient_id:
    consultation_data = {
        "patient": patient_id,
        "notes": "Patient has a common cold",
        "medicines": [
            {
                "medicine_id": 1,
                "instructions": "Take one tablet twice daily"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/doctor/consultations/", json=consultation_data, headers=doctor_headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ Consultation created successfully")
    else:
        print(f"   ✗ Failed: {response.text[:100]}")
else:
    print("   ⊘ Skipped (no patient ID available)")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✓ All routes tested")
print("\nRoutes Summary:")
print("Frontend:")
print("  - / (Login)")
print("  - /admin (Admin Dashboard)")
print("  - /admin/doctors (Doctor List)")
print("  - /admin/add-doctor (Add Doctor)")
print("  - /admin/medicines (Medicine List)")
print("  - /doctor (Doctor Dashboard)")
print("  - /doctor/patients (Patient List)")
print("  - /doctor/add-patient (Add Patient)")
print("  - /doctor/consult (Add Consultation)")
print("  - /doctor/history (Consultation History)")
print("\nBackend APIs:")
print("  - POST /api/login/")
print("  - GET/POST /api/admin/doctors/")
print("  - GET/POST /api/admin/medicines/")
print("  - GET/POST /api/doctor/patients/")
print("  - GET/POST /api/doctor/consultations/")
print("  - GET /api/doctor/consultations/history/")
