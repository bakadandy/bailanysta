from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm, ProfilePictureForm
from .serializers import UserSerializer, ProfileUpdateSerializer, PasswordChangeSerializer
from posts.models import Post
from django.contrib import messages


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'nickname']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def get_serializer_class(self):
        if self.action == 'update_profile':
            return ProfileUpdateSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        return UserSerializer
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        if request.user.is_authenticated:
            if request.user == user_to_follow:
                return Response(
                    {"error": "You cannot follow yourself"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if request.user in user_to_follow.user_followers.all():
                user_to_follow.user_followers.remove(request.user)
                return Response({"status": "unfollowed"}, status=status.HTTP_200_OK)
            else:
                user_to_follow.user_followers.add(request.user)
                return Response({"status": "following"}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Authentication required"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = user.user_followers.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        following = user.user_following.all()
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                request.user.set_password(serializer.validated_data['new_password'])
                request.user.save()
                # Update session so user stays logged in
                update_session_auth_hash(request, request.user)
                return Response({"status": "password changed"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            error_message = "Invalid username or password."
            return render(request, 'users/login.html', {'error_message': error_message})
    return render(request, 'users/login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:home')


@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    
    # Check if this is the current user's profile
    is_own_profile = request.user == user
    
    # Handle profile picture upload if it's the user's own profile
    if is_own_profile and request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('users:profile', username=username)
    else:
        form = ProfilePictureForm(instance=user) if is_own_profile else None
    
    context = {
        'profile_user': user,
        'posts': posts,
        'is_own_profile': is_own_profile,
        'picture_form': form,
    }
    return render(request, 'users/profile.html', context)


def terms_and_conditions(request):
    return render(request, 'users/terms_cond.html')


@login_required
def connections_view(request):
    """View for displaying user connections (followers and following)"""
    # We'll load the data via AJAX, so we just render the template
    return render(request, 'users/connections.html')


