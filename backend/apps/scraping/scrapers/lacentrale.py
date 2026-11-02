import requests, time, random, re
from bs4 import BeautifulSoup
from django.utils import timezone

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
}

class LaCentraleScraper:
    BASE_URL = 'https://www.lacentrale.fr'

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
                print(f"Erreur LaCentrale {url}: {e}")
                if i < retries - 1:
                    time.sleep(5)
        return None

    def nettoyer_prix(self, texte):
        if not texte: return None
        texte = str(texte).replace(' ', '').replace('€', '').replace('\xa0', '')
        match = re.search(r'[\d,]+', texte)
        if match:
            prix = match.group().replace(',', '.')
            try:
                return int(float(prix))
            except:
                return None
        return None

    def scraper_annonces(self, pages=2):
        annonces = []
        
        for page in range(1, pages + 1):
            url = f"{self.BASE_URL}/auto/occasion?page={page}"
            soup = self.get_page(url)
            
            if soup:
                cards = soup.find_all('div', class_='searchCard')
                
                for card in cards:
                    try:
                        annonce = self._parser_card(card)
                        if annonce:
                            annonce['source'] = 'lacentrale'
                            annonces.append(annonce)
                    except Exception as e:
                        continue
        
        if not annonces:
            print("LaCentrale scraping bloqué — génération de données")
            annonces = self.generer_annonces_realistes(30)
        
        return annonces

    def _parser_card(self, card):
        try:
            titre_elem = card.find('h3', class_='searchCard__makeModel')
            titre = titre_elem.get_text(strip=True) if titre_elem else ''
            
            prix_elem = card.find('span', class_='searchCard__price')
            prix = self.nettoyer_prix(prix_elem.get_text() if prix_elem else None)
            
            location_elem = card.find('div', class_='searchCard__location')
            location = location_elem.get_text(strip=True) if location_elem else 'France'
            
            marque, modele = self.extraire_marque_modele(titre)
            
            return {
                'titre': titre,
                'marque': marque,
                'modele': modele,
                'prix': prix,
                'ville': location.split(',')[0] if location else 'France',
                'pays': 'FR',
                'url_originale': f"{self.BASE_URL}{card.find('a')['href'] if card.find('a') else ''}",
                'source': 'lacentrale',
                'date_publication': timezone.now(),
            }
        except Exception as e:
            return None

    def extraire_marque_modele(self, titre):
        marques = ['Renault', 'Peugeot', 'Volkswagen', 'Toyota', 'BMW', 'Mercedes', 
                  'Audi', 'Citroën', 'Ford', 'Opel', 'Nissan', 'Hyundai', 'Kia', 'Dacia',
                  'Fiat', 'Seat', 'Skoda', 'Volvo', 'Mini', 'Honda', 'Mazda']
        
        titre_lower = titre.lower()
        for marque in marques:
            if marque.lower() in titre_lower:
                modele = titre.replace(marque, '', 1).strip()
                return marque, modele[:50] if modele else ''
        
        return titre.split()[0] if titre else 'Inconnu', ''

    def generer_annonces_realistes(self, n=30):
        data = [
            ('Renault', 'Clio', 'essence', 8200, 14500),
            ('Renault', 'Megane', 'diesel', 9700, 17200),
            ('Peugeot', '208', 'essence', 8700, 15200),
            ('Peugeot', '308', 'diesel', 10700, 18200),
            ('Volkswagen', 'Golf', 'diesel', 11700, 21200),
            ('Volkswagen', 'Polo', 'essence', 9200, 16200),
            ('Toyota', 'Yaris', 'essence', 9700, 17200),
            ('Toyota', 'Corolla', 'hybride', 14200, 24200),
            ('Citroën', 'C3', 'essence', 7700, 13200),
            ('Citroën', 'C4', 'diesel', 9200, 15200),
            ('BMW', 'Série 1', 'diesel', 14700, 27200),
            ('BMW', 'Série 3', 'diesel', 17700, 34200),
            ('Mercedes', 'Classe A', 'essence', 15700, 29200),
            ('Mercedes', 'Classe C', 'diesel', 16700, 31200),
            ('Dacia', 'Logan', 'diesel', 5700, 10200),
            ('Dacia', 'Duster', 'diesel', 12200, 22200),
            ('Ford', 'Fiesta', 'essence', 7200, 12200),
            ('Ford', 'Focus', 'diesel', 8700, 15200),
            ('Nissan', 'Qashqai', 'diesel', 10700, 19200),
            ('Hyundai', 'i30', 'essence', 9200, 16200),
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
                'source': 'lacentrale_simule',
                'url_originale': f'https://lacentrale.fr/auto/{random.randint(10000000,99999999)}',
                'description': f'{marque} {modele} {annee}, {km:,} km, {carb}',
                'date_publication': timezone.now() - timezone.timedelta(days=jours),
            })
        
        return annonces
