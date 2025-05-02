from django.db import models
from posts.models import Post
from users.models import User

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(verbose_name='Post', to=Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name='Content', max_length=500)
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated At', auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'