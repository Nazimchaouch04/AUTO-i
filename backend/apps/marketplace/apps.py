from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.marketplace'
    verbose_name = 'Marketplace Automobile'


class MarketplaceFixedConfig(AppConfig):
    default_auto_field = 'created_at'
    name = 'apps.marketplace_fixed'
    verbose_name = 'Marketplace Fixed'
    
    def ready(self):
        """Initialisation de l'application"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Application Marketplace Fixed initialisée")
