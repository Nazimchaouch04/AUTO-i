from celery import shared_task
from django.db import transaction
from apps.annonces.models import Annonce, Vehicule
from .scrapers.ouedkniss import OuedknissScraper

@shared_task(name='scraping.scraper_annonces')
def scraper_annonces_task():
    scraper = OuedknissScraper()
    annonces_data = scraper.scraper_annonces(pages=5)
    crees = 0
    erreurs = 0

    for data in annonces_data:
        try:
            with transaction.atomic():
                vehicule, _ = Vehicule.objects.get_or_create(
                    marque=data['marque'], modele=data['modele'],
                    defaults={'categorie': 'berline'})

                annonce, created = Annonce.objects.get_or_create(
                    url_originale=data['url_originale'],
                    defaults={
                        'vehicule': vehicule,
                        'annee': data['annee'],
                        'kilometrage': data['kilometrage'],
                        'carburant': data['carburant'],
                        'boite': data.get('boite', 'manuelle'),
                        'puissance': data.get('puissance'),
                        'prix': data['prix'],
                        'ville': data.get('ville', ''),
                        'pays': data.get('pays', 'DZ'),
                        'source': data.get('source', 'scraping'),
                        'description': data.get('description', ''),
                        'date_publication': data.get('date_publication'),
                    })

                if created:
                    from apps.estimation.ml_model import get_modele
                    modele = get_modele()
                    result = modele.estimer(
                        marque=data['marque'], annee=data['annee'],
                        kilometrage=data['kilometrage'],
                        carburant=data['carburant'],
                        boite=data.get('boite', 'manuelle'),
                        puissance=data.get('puissance', 100),
                        pays=data.get('pays', 'DZ'),
                    )
                    annonce.prix_estime = result['prix_estime']
                    annonce.ecart_prix = round(
                        (float(annonce.prix) - result['prix_estime'])
                        / result['prix_estime'] * 100, 1)
                    score = 0
                    if annonce.ecart_prix <= -20: score += 50
                    elif annonce.ecart_prix <= -10: score += 25
                    elif annonce.ecart_prix <= -5: score += 10
                    age = 2025 - annonce.annee
                    km_an = annonce.kilometrage / max(age, 1)
                    if km_an < 10000: score += 15
                    annonce.score_affaire = score
                    annonce.est_bonne_affaire = score >= 40
                    annonce.save()
                    crees += 1
        except Exception as e:
            erreurs += 1

    return f'{crees} nouvelles annonces créées, {erreurs} erreurs'
