from rest_framework.routers import DefaultRouter
from .views import MarqueViewSet, AnnonceViewSet

router = DefaultRouter()
router.register(r'marques', MarqueViewSet, basename='marque')
router.register(r'', AnnonceViewSet, basename='annonce')
urlpatterns = router.urls
