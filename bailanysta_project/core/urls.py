from django.urls import path
from .views import HomeView
from . import views

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ai/generate-content/', views.generate_ai_content, name='generate_ai_content'),
    path('ai/suggest-hashtags/', views.get_hashtag_suggestions, name='suggest_hashtags'),
]

