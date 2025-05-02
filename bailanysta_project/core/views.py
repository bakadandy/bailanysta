from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import TemplateView
from .serializers import UserSerializer
from users.models import User
from posts.models import Post

# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/home.html'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created_at')[:10]
        return context

# API ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

