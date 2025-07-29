from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    # Authentication
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='gallery/login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),
    path('register/', views.register_view, name='register'),
    
    # Dashboard & Photos
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-photos/', views.my_photos, name='my_photos'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photo/<uuid:pk>/', views.photo_detail, name='photo_detail'),
    path('photo/<uuid:pk>/edit/', views.edit_photo, name='edit_photo'),
    path('photo/<uuid:pk>/delete/', views.delete_photo, name='delete_photo'),
    path('photo/<uuid:pk>/like/', views.like_photo, name='like_photo'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Albums
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('albums/create/', views.AlbumCreateView.as_view(), name='album_create'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('albums/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album_edit'),
]