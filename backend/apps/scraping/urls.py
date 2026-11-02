from django.urls import path
from .views import ScrapingAPIView

urlpatterns = [
    path('', ScrapingAPIView.as_view(), name='scraping_api'),
]
