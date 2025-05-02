from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm
from .serializers import UserSerializer
from posts.models import Post


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
    posts = Post.objects.filter(author=user).order_by('-created_at')
    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'users/profile.html', context)


