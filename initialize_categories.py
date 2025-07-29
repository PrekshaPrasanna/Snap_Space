import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photogallery.settings')
django.setup()

from gallery.models import Category

# Default categories
DEFAULT_CATEGORIES = [
    'Nature',
    'Animals',
    'Food',
    'Architecture',
    'People',
    'Travel',
    'Sports',
    'Technology',
    'Art'
]

def initialize_categories():
    """Create default categories if they don't exist"""
    for category_name in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(name=category_name)
    
    count = Category.objects.count()
    print(f"Categories initialized. Total categories: {count}")

if __name__ == '__main__':
    initialize_categories()