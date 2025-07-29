from django.contrib import admin
from .models import Category, Photo, UserProfile, Album

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_shared', 'created_at')
    list_filter = ('is_shared', 'created_at')
    search_fields = ('name', 'user__username')