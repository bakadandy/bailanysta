from django.urls import path
from .views import CommentViewSet

app_name = 'comments'

urlpatterns = [
    path('', CommentViewSet.as_view({'get': 'list'}), name='comment_list'),
    path('<int:pk>/', CommentViewSet.as_view({'get': 'retrieve'}), name='comment_detail'),
]
