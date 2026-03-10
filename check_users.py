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

# Check all users
users = User.objects.all()
print(f"Total users in database: {users.count()}")
for user in users:
    print(f"  - Username: {user.username}, Role: {user.role}, Is Active: {user.is_active}")

# Try to authenticate
print("\nTesting authentication...")
user = authenticate(username='admin', password='admin123')
if user:
    print(f"✓ Authentication successful for admin")
    print(f"  User: {user.username}")
    print(f"  Role: {user.role}")
else:
    print("✗ Authentication failed for admin")
    
    # Check if user exists
    try:
        admin_user = User.objects.get(username='admin')
        print(f"\nUser 'admin' exists:")
        print(f"  Is active: {admin_user.is_active}")
        print(f"  Password set: {bool(admin_user.password)}")
    except User.DoesNotExist:
        print("\nUser 'admin' does not exist in database!")
