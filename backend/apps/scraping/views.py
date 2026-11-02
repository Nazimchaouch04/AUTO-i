from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .scrapers.manager import ScrapingManager

class ScrapingAPIView(APIView):
    """API pour le scraping multi-sources"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Lance le scraping de toutes les sources"""
        try:
            manager = ScrapingManager()
            pages = int(request.query_params.get('pages', 2))
            
            # Optionnel: scraper une source spécifique
            source = request.query_params.get('source')
            
            if source:
                annonces = manager.scraper_source_specifique(source, pages)
            else:
                annonces = manager.scraper_toutes_sources(pages)
            
            return Response({
                'success': True,
                'total': len(annonces),
                'annonces': annonces[:100],  # Limiter à 100 pour la réponse
                'sources': manager.get_sources_disponibles()
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    def options(self, request):
        """Retourne les sources disponibles"""
        manager = ScrapingManager()
        return Response({
            'sources': manager.get_sources_disponibles()
        })
