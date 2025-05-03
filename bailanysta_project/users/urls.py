from django.urls import path
from .views import UserViewSet, login_view, register_view, logout_view, profile_view, terms_and_conditions, connections_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('register/terms/', terms_and_conditions, name='terms_conditions'),
    path('connections/', connections_view, name='connections'),
]