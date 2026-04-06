from django.urls import path
from .views import ProfilJoueurViewSet, TransactionViewSet, DefiViewSet, BoutiqueViewSet

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
shop_list_view = BoutiqueViewSet.as_view({
    'get': 'list'
})
shop_buy_view = BoutiqueViewSet.as_view({
    'post': 'buy'
})

urlpatterns = [
    path('profil/', profil_view, name='profil'),
    path('profil/add-coins/', add_coins_view, name='add_coins'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('transactions/', transactions_view, name='transactions'),
    path('defis/', defis_view, name='defis'),
    path('shop/', shop_list_view, name='shop_list'),
    path('shop/<int:pk>/buy/', shop_buy_view, name='shop_buy'),
]
