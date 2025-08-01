# Generated by Django 5.1.4 on 2025-03-18 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='profile_pic',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics/'),
        ),
    ]
