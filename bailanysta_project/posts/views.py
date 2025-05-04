from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer

# Create your views here.

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'hashtags']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        following = self.request.query_params.get('following', None)
        if following and self.request.user.is_authenticated:
            followed_users = self.request.user.user_following.all()
            queryset = queryset.filter(user__in=followed_users)
        
        # Add hashtag filtering
        hashtag = self.request.query_params.get('hashtag', None)
        if hashtag:
            # Remove # if present
            if hashtag.startswith('#'):
                hashtag = hashtag[1:]
            queryset = queryset.filter(hashtags__contains=hashtag)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        List posts with optional hashtag filtering, supporting both HTML and API responses
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Check if 'format' parameter is set (DRF uses this for API format)
        # If not specified, assume HTML rendering is wanted (for browser)
        if request.GET.get('format', None) is None and not request.accepted_media_type == 'application/json':
            # For browser requests, render the template            
            return render(request, 'posts/post_list.html', {
                'posts': queryset,
                'request': request,
            })
        else:
            # For API requests, return JSON
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def user_feed(self, request):
        """Get posts from the user and users they follow"""
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
            
        following_users = request.user.user_following.all()
        
        queryset = self.queryset.filter(user__in=list(following_users) + [request.user])
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search_hashtags(self, request):
        """Search posts by hashtag"""
        hashtag = request.query_params.get('tag', None)
        if not hashtag:
            return Response({"error": "Hashtag is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove # if present
        if hashtag.startswith('#'):
            hashtag = hashtag[1:]
            
        queryset = self.queryset.filter(hashtags__contains=hashtag)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


