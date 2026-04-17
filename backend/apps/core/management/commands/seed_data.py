from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed initial data for development'

    def handle(self, *args, **options):
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@autointel.dz',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superuser "admin" créé'))
        else:
            self.stdout.write('Superuser "admin" existe déjà')

        self.stdout.write(self.style.SUCCESS('Seed data terminé ✓'))
