import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s UserProfile"

class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    likes = models.ManyToManyField(User, related_name='liked_photos', blank=True)

    def __str__(self):
        return f"{self.user.username}'s UserProfile"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('photo_detail', args=[str(self.id)])
    
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-created_at']

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=255)
    photos = models.ManyToManyField(Photo, related_name='albums', blank=True)
    is_shared = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"