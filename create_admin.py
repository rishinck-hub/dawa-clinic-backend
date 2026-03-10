#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_backend.settings')
sys.path.insert(0, 'd:\\Projects\\dawa_clinic\\backend\\clinic_backend')

django.setup()

from accounts.models import User

# Check if admin user already exists
if User.objects.filter(username='admin').exists():
    print("✓ Admin user already exists!")
else:
    # Create admin user
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@clinic.com',
        password='admin123',
        role='ADMIN',
        first_name='Admin',
        last_name='User'
    )
    print("✓ Admin user created successfully!")
    print(f"  Username: admin")
    print(f"  Password: admin123")
    print(f"  Role: ADMIN")

# Also create a test doctor user
if User.objects.filter(username='doctor').exists():
    print("✓ Doctor user already exists!")
else:
    doctor_user = User.objects.create_user(
        username='doctor',
        email='doctor@clinic.com',
        password='doctor123',
        role='DOCTOR',
        first_name='Dr.',
        last_name='Smith'
    )
    print("✓ Doctor user created successfully!")
    print(f"  Username: doctor")
    print(f"  Password: doctor123")
    print(f"  Role: DOCTOR")

print("\n✅ Initial users setup complete!")
