from django.urls import path
from .views import ProfilJoueurViewSet, TransactionViewSet, DefiViewSet

profil_view = ProfilJoueurViewSet.as_view({
    'get': 'profil'
})
add_coins_view = ProfilJoueurViewSet.as_view({
    'post': 'add_coins'
})
leaderboard_view = ProfilJoueurViewSet.as_view({
    'get': 'leaderboard'
})
transactions_view = TransactionViewSet.as_view({
    'get': 'list'
})
defis_view = DefiViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
    path('profil/', profil_view, name='profil'),
    path('profil/add-coins/', add_coins_view, name='add_coins'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('transactions/', transactions_view, name='transactions'),
    path('defis/', defis_view, name='defis'),
]
