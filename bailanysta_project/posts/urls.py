from django.urls import path
from .views import PostViewSet

app_name = 'posts'

urlpatterns = [
    path('', PostViewSet.as_view({'get': 'list'}), name='post_list'),
    path('<int:pk>/', PostViewSet.as_view({'get': 'retrieve'}), name='post_detail'),
]
