"""
Manager multi-sources pour le scraping automobile
Agrège les données de plusieurs plateformes
"""

from .ouedkniss import OuedknissScraper
from .leboncoin import LeBonCoinScraper
from .autoscout24 import AutoScout24Scraper
from .lacentrale import LaCentraleScraper

class ScrapingManager:
    """Gère le scraping multi-sources"""
    
    def __init__(self):
        self.scrapers = {
            'ouedkniss': OuedknissScraper(),
            'leboncoin': LeBonCoinScraper(),
            'autoscout24': AutoScout24Scraper(),
            'lacentrale': LaCentraleScraper(),
        }
    
    def scraper_toutes_sources(self, pages=2):
        """Scrape toutes les sources configurées"""
        toutes_annonces = []
        
        for source_name, scraper in self.scrapers.items():
            print(f"🔍 Scraping {source_name}...")
            try:
                annonces = scraper.scraper_annonces(pages=pages)
                print(f"✅ {source_name}: {len(annonces)} annonces trouvées")
                toutes_annonces.extend(annonces)
            except Exception as e:
                print(f"❌ Erreur {source_name}: {e}")
        
        print(f"\n📊 Total: {len(toutes_annonces)} annonces de toutes les sources")
        return toutes_annonces
    
    def scraper_source_specifique(self, source, pages=2):
        """Scrape une source spécifique"""
        if source not in self.scrapers:
            raise ValueError(f"Source {source} non disponible")
        
        scraper = self.scrapers[source]
        return scraper.scraper_annonces(pages=pages)
    
    def get_sources_disponibles(self):
        """Retourne la liste des sources disponibles"""
        return list(self.scrapers.keys())
