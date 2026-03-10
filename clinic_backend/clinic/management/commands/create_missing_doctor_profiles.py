from django.core.management.base import BaseCommand
from django.db.models import Q
from accounts.models import User
from clinic.models import Doctor


class Command(BaseCommand):
    help = 'Create missing Doctor profiles for doctor users'

    def handle(self, *args, **options):
        # Find all doctor users without a Doctor profile
        doctor_users = User.objects.filter(role='DOCTOR')
        created_count = 0
        
        for user in doctor_users:
            doctor, was_created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'name': user.username,
                    'specialization': 'General',
                    'phone': '',
                    'email': '',
                }
            )
            if was_created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created Doctor profile for user: {user.username}'
                    )
                )
        
        if created_count == 0:
            self.stdout.write(
                self.style.SUCCESS('All doctor users have profiles.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {created_count} missing Doctor profiles.'
                )
            )
