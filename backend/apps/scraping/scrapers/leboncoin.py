import requests, time, random, re
from bs4 import BeautifulSoup
from django.utils import timezone

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

class LeBonCoinScraper:
    BASE_URL = 'https://www.leboncoin.fr'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_page(self, url, retries=3):
        for i in range(retries):
            try:
                time.sleep(random.uniform(1, 3))
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    return BeautifulSoup(resp.text, 'html.parser')
            except Exception as e:
                print(f"Erreur LeBonCoin {url}: {e}")
                if i < retries - 1:
                    time.sleep(5)
        return None

    def nettoyer_prix(self, texte):
        if not texte: return None
        # Enlever les espaces et convertir en nombre
        texte = str(texte).replace(' ', '').replace('€', '').replace('\xa0', '')
        match = re.search(r'[\d,]+', texte)
        if match:
            prix = match.group().replace(',', '.')
            try:
                return int(float(prix))
            except:
                return None
        return None

    def scraper_annonces(self, pages=3):
        annonces = []
        
        # Catégorie voitures
        categories = ['voitures', 'utilitaires']
        
        for category in categories:
            for page in range(1, pages + 1):
                url = f"{self.BASE_URL}/{category}/offres/p-{page}"
                soup = self.get_page(url)
                
                if soup:
                    # LeBonCoin utilise des data attributes
                    cards = soup.find_all('a', {'data-test': 'ad-card'})
                    
                    for card in cards:
                        try:
                            annonce = self._parser_card(card)
                            if annonce:
                                annonce['source'] = 'leboncoin'
                                annonces.append(annonce)
                        except Exception as e:
                            continue
        
        # Si scraping bloqué ou pas de résultats, générer des données
        if not annonces:
            print("LeBonCoin scraping bloqué — génération de données")
            annonces = self.generer_annonces_realistes(50)
        
        return annonces

    def _parser_card(self, card):
        try:
            # Titre
            titre = card.get('title', '')
            if not titre:
                titre_elem = card.find(['h2', 'h3'])
                titre = titre_elem.get_text(strip=True) if titre_elem else ''
            
            # Prix
            prix_elem = card.find(['span', 'p'], {'data-test': 'price'})
            prix = self.nettoyer_prix(prix_elem.get_text() if prix_elem else None)
            
            # Localisation
            location_elem = card.find(['p', 'span'], {'data-test': 'location'})
            location = location_elem.get_text(strip=True) if location_elem else 'France'
            
            # Extraire marque et modèle du titre
            marque, modele = self.extraire_marque_modele(titre)
            
            return {
                'titre': titre,
                'marque': marque,
                'modele': modele,
                'prix': prix,
                'ville': location.split(',')[0] if location else 'France',
                'pays': 'FR',
                'url_originale': f"{self.BASE_URL}{card.get('href', '')}",
                'source': 'leboncoin',
                'date_publication': timezone.now(),
            }
        except Exception as e:
            print(f"Erreur parsing LeBonCoin: {e}")
            return None

    def extraire_marque_modele(self, titre):
        # Liste des marques communes
        marques = ['Renault', 'Peugeot', 'Volkswagen', 'Toyota', 'BMW', 'Mercedes', 
                  'Audi', 'Citroën', 'Ford', 'Opel', 'Nissan', 'Hyundai', 'Kia', 'Dacia',
                  'Fiat', 'Seat', 'Skoda', 'Volvo', 'Mini', 'Honda', 'Mazda']
        
        titre_lower = titre.lower()
        for marque in marques:
            if marque.lower() in titre_lower:
                # Extraire le modèle (ce qui suit la marque)
                modele = titre.replace(marque, '', 1).strip()
                return marque, modele[:50] if modele else ''
        
        return titre.split()[0] if titre else 'Inconnu', ''

    def generer_annonces_realistes(self, n=50):
        """Génère des annonces réalistes pour le marché français"""
        data = [
            ('Renault', 'Clio', 'essence', 8500, 15000),
            ('Renault', 'Megane', 'diesel', 10000, 18000),
            ('Peugeot', '208', 'essence', 9000, 16000),
            ('Peugeot', '308', 'diesel', 11000, 19000),
            ('Volkswagen', 'Golf', 'diesel', 12000, 22000),
            ('Volkswagen', 'Polo', 'essence', 9500, 17000),
            ('Toyota', 'Yaris', 'essence', 10000, 18000),
            ('Toyota', 'Corolla', 'hybride', 15000, 25000),
            ('Citroën', 'C3', 'essence', 8000, 14000),
            ('Citroën', 'C4', 'diesel', 9500, 16000),
            ('BMW', 'Série 1', 'diesel', 15000, 28000),
            ('BMW', 'Série 3', 'diesel', 18000, 35000),
            ('Mercedes', 'Classe A', 'essence', 16000, 30000),
            ('Mercedes', 'Classe C', 'diesel', 17000, 32000),
            ('Audi', 'A3', 'diesel', 14000, 26000),
            ('Dacia', 'Logan', 'diesel', 6000, 11000),
            ('Dacia', 'Sandero', 'essence', 7000, 12000),
            ('Ford', 'Fiesta', 'essence', 7500, 13000),
            ('Ford', 'Focus', 'diesel', 9000, 16000),
            ('Nissan', 'Qashqai', 'diesel', 11000, 20000),
        ]
        
        villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes', 
                  'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille']
        
        annonces = []
        for _ in range(n):
            marque, modele, carb, prix_min, prix_max = random.choice(data)
            annee = random.randint(2010, 2023)
            age = 2025 - annee
            km = random.randint(age * 10000, age * 25000)
            prix = int(random.randint(prix_min, prix_max) * random.uniform(0.85, 1.20))
            jours = random.randint(0, 30)
            ville = random.choice(villes)
            
            annonces.append({
                'titre': f'{marque} {modele} {annee}',
                'marque': marque,
                'modele': modele,
                'annee': annee,
                'kilometrage': km,
                'carburant': carb,
                'boite': random.choice(['manuelle', 'automatique']),
                'puissance': random.randint(70, 200),
                'prix': prix,
                'ville': ville,
                'pays': 'FR',
                'source': 'leboncoin_simule',
                'url_originale': f'https://leboncoin.fr/voitures/{random.randint(10000000,99999999)}',
                'description': f'{marque} {modele} {annee}, {km:,} km, {carb}, {ville}',
                'date_publication': timezone.now() - timezone.timedelta(days=jours),
            })
        
        return annonces
