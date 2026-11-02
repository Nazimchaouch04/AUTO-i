from django.urls import path
from .views import RegisterView, MeView, ChangePasswordView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('users/', UserListView.as_view()),
]
