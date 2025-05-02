from django.db import models
from users.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name='Content', max_length=500)
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated At', auto_now=True)
    likes = models.ManyToManyField(verbose_name='Likes', to=User, related_name='liked_posts')

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'