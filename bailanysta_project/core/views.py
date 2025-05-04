from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import TemplateView
from .serializers import UserSerializer
from users.models import User
from posts.models import Post
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .ai_helpers import generate_post_content, suggest_hashtags

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_content(request):
    """
    Generate AI content based on prompt
    """
    prompt = request.data.get('prompt', '')
    max_length = request.data.get('max_length', 280)
    
    if not prompt:
        return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    generated_content = generate_post_content(prompt, max_length)
    
    return Response({
        'content': generated_content
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_hashtag_suggestions(request):
    """
    Get hashtag suggestions for post content
    """
    content = request.data.get('content', '')
    max_hashtags = request.data.get('max_hashtags', 5)
    
    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    hashtags = suggest_hashtags(content, max_hashtags)
    
    return Response({
        'hashtags': hashtags
    })

