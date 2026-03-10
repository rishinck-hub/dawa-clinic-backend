import os
from django.apps import AppConfig
from django.db import OperationalError, ProgrammingError


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        # Create a default admin account if it doesn't exist.
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
        except Exception:
            return

        username = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
        password = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

        try:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "role": "ADMIN",
                    "is_staff": True,
                    "is_superuser": True,
                    "email": os.getenv("DEFAULT_ADMIN_EMAIL", ""),
                },
            )
            if created:
                user.set_password(password)
                user.save()
        except (OperationalError, ProgrammingError):
            # Database might not be ready during migrations/startup.
            return
