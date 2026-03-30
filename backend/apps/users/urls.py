from django.urls import path
from .views import RegisterView, UserProfileView

register_view = RegisterView.as_view({
    'post': 'register'
})
profile_view = UserProfileView.as_view({
    'get': 'profile',
    'put': 'profile'
})

urlpatterns = [
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
]
