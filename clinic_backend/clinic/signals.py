from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import Doctor


@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    """
    Create a Doctor profile when a user with role='DOCTOR' is created.
    This ensures every doctor user has a corresponding Doctor profile.
    """
    if created and instance.role == 'DOCTOR':
        # Only create if it doesn't already exist
        if not hasattr(instance, 'doctor'):
            Doctor.objects.get_or_create(
                user=instance,
                defaults={
                    'name': instance.username,
                    'specialization': 'General',
                    'phone': '',
                    'email': '',
                }
            )
