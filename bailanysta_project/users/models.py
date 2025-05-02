from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    profile_picture = models.ImageField(verbose_name='Profile Picture', upload_to='profile_pictures/', null=True, blank=True)
    nickname = models.CharField(verbose_name='Nickname', max_length=255, null=True, blank=True)
    bio = models.TextField(verbose_name='Bio', max_length=500, null=True, blank=True)
    user_followers = models.ManyToManyField('self', 
                                      symmetrical=False, 
                                      related_name='user_following',
                                      verbose_name='Followers')

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
