from django.core.management.base import BaseCommand
from apps.estimation.ml_model import get_modele

class Command(BaseCommand):
    help = "Entraîne le modèle ML d'estimation de prix"

    def handle(self, *args, **options):
        self.stdout.write('Entraînement du modèle...')
        modele = get_modele()
        stats = modele.entrainer()
        self.stdout.write(self.style.SUCCESS(
            f'Modèle entraîné: MAE={stats["mae"]}€, R²={stats["r2"]}, N={stats["n_samples"]}'
        ))
