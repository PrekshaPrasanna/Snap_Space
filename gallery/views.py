from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Photo, UserProfile, Category, UserProfile, Album
from .forms import CustomUserCreationForm, PhotoForm, UserProfileForm, UserForm, AlbumForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

def my_view(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, "my_template.html", {"categories": categories})

def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"profile": profile})

def index(request):
    """Landing page view"""
    return render(request, 'gallery/index.html')

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'gallery/register.html', {'form': form})

@login_required
def dashboard(request):
    """Dashboard view showing all photos"""
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    photos = Photo.objects.all()
    
    # Filter by search query
    if search_query:
        photos = photos.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    if category:
        photos = photos.filter(category__name=category)
    
    categories = Category.objects.all()
    
    context = {
        'photos': photos,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
    }
    
    return render(request, 'gallery/dashboard.html', context)

@login_required
def my_photos(request):
    """View showing only the user's photos"""
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    photos = Photo.objects.filter(user=request.user)
    
    # Filter by search query
    if search_query:
        photos = photos.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    if category:
        photos = photos.filter(category__name=category)
    
    categories = Category.objects.all()
    
    context = {
        'photos': photos,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
    }
    
    return render(request, 'gallery/my_photos.html', context)

@login_required
def upload_photo(request):
    """View for uploading a new photo"""
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('my_photos')
    else:
        form = PhotoForm()
    
    return render(request, 'gallery/upload_photo.html', {'form': form})

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    user = request.user
    
    # Check if user has already liked the photo
    if photo.likes.filter(id=user.id).exists():
        # User has already liked this photo, so remove the like
        photo.likes.remove(user)
        liked = False
    else:
        # User hasn't liked this photo, so add the like
        photo.likes.add(user)
        liked = True
    
    return JsonResponse({
        'status': 'success',
        'liked': liked,
        'likes_count': photo.likes.count()
    })

@login_required
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = photo.likes.filter(id=request.user.id).exists()

    liked_users = None
    if request.user == photo.user:
        liked_users = photo.likes.all()

    context = {
        'photo': photo,
        'user_has_liked': user_has_liked,
        'confirm_delete': request.GET.get('confirm_delete', False),
        'liked_users': liked_users,
    }
    return render(request, 'gallery/photo_detail.html', context)

@login_required
def edit_photo(request, pk):
    """View for editing a photo"""
    photo = get_object_or_404(Photo, pk=pk)
    
    # Check if the user is the owner of the photo
    if photo.user != request.user:
        messages.error(request, "You don't have permission to edit this photo.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo updated successfully!')
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm(instance=photo)
    
    return render(request, 'gallery/upload_photo.html', {'form': form, 'edit_mode': True})

@login_required
def delete_photo(request, pk):
    """View for deleting a photo"""
    photo = get_object_or_404(Photo, pk=pk)
    
    # Check if the user is the owner of the photo
    if photo.user != request.user:
        messages.error(request, "You don't have permission to delete this photo.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('my_photos')
    
    # Show a separate confirmation page
    return render(request, 'gallery/confirm_delete.html', {'photo': photo})

def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"profile": profile})

@login_required
def logout_page(request):
    return render(request, 'gallery/logout.html')

@login_required
def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'gallery/logout_confirm.html')
    return redirect('dashboard')

def dashboard(request):
    search_query = request.GET.get('search', '')
    selected_category = request.GET.get('category', '')

    photos = Photo.objects.all()

    if search_query:
        photos = photos.filter(title__icontains=search_query)
    
    if selected_category:
        photos = photos.filter(category__id=selected_category)

    categories = Category.objects.all()

    return render(request, 'gallery/dashboard.html', {
        'photos': photos,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category
    })

class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'

    def get_queryset(self):
        # Show user's own albums and all shared albums
        return Album.objects.filter(
            Q(user=self.request.user) | Q(is_shared=True)
        ).distinct()

class AlbumDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'

    def test_func(self):
        album = self.get_object()
        return album.is_shared or album.user == self.request.user

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    success_url = '/albums/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show 'is_shared' if the user is the creator
        if self.request.user != self.object.user if hasattr(self, 'object') and self.object else self.request.user != self.request.user:
            form.fields.pop('is_shared', None)
        return form

class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    success_url = '/albums/'

    def test_func(self):
        album = self.get_object()
        # Only the owner can edit, regardless of is_shared
        return album.user == self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        album = self.get_object()
        # Only show 'is_shared' if the user is the owner
        if self.request.user != album.user:
            form.fields.pop('is_shared', None)
        return form
