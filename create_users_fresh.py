#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_backend.settings')
sys.path.insert(0, 'd:\\Projects\\dawa_clinic\\backend\\clinic_backend')

django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

# Delete old users
User.objects.filter(username='admin').delete()
User.objects.filter(username='your_admin_name').delete()
User.objects.filter(username='doctor').delete()

print("✓ Deleted old users")

# Create new admin user
admin_user = User.objects.create_user(
    username='admin',
    email='admin@clinic.com',
    password='admin123',
    role='ADMIN',
    first_name='Admin',
    last_name='User'
)
print(f"✓ Admin user created!")
print(f"  Username: admin")
print(f"  Password: admin123")
print(f"  Role: {admin_user.role}")

# Create test doctor user
doctor_user = User.objects.create_user(
    username='doctor',
    email='doctor@clinic.com',
    password='doctor123',
    role='DOCTOR',
    first_name='Dr.',
    last_name='Smith'
)
print(f"✓ Doctor user created!")
print(f"  Username: doctor")
print(f"  Password: doctor123")
print(f"  Role: {doctor_user.role}")

# Test authentication
print("\n✓ Testing authentication...")
user = authenticate(username='admin', password='admin123')
if user:
    print(f"✓ Authentication successful!")
    print(f"  Username: {user.username}")
    print(f"  Role: {user.role}")
else:
    print("✗ Authentication failed!")
