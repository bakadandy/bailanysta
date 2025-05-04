from django.db import models
from users.models import User
import re

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name='Content', max_length=500)
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated At', auto_now=True)
    likes = models.ManyToManyField(verbose_name='Likes', to=User, related_name='liked_posts')
    hashtags = models.CharField(verbose_name='Hashtags', max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    
    def save(self, *args, **kwargs):
        # Extract hashtags from content
        hashtag_pattern = re.compile(r'#(\w+)')
        hashtags = hashtag_pattern.findall(self.content)
        self.hashtags = ' '.join(hashtags)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'