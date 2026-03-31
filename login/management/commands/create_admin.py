import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create a default admin superuser from environment variables"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_PASSWORD not set, skipping admin creation."
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                f'Admin user "{username}" already exists, skipping.'
            ))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(
            f'Superuser "{username}" created successfully!'
        ))
