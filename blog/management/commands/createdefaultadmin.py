from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = """creates default super user account based on ENV"""
    def handle(self, *args, **options):
        user = os.environ['ADMIN_USERNAME']
        email = os.environ['ADMIN_EMAIL']
        password = os.environ['ADMIN_PASSWORD']

        if not User.objects.filter(username=user).exists():
            User.objects.create_superuser(user, email, password)
