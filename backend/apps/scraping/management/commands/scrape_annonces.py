from django.core.management.base import BaseCommand
from apps.scraping.tasks import scraper_annonces_task

class Command(BaseCommand):
    help = 'Lance le scraping des annonces automobiles'
    def handle(self, *args, **options):
        self.stdout.write('Scraping en cours...')
        result = scraper_annonces_task()
        self.stdout.write(self.style.SUCCESS(result))
