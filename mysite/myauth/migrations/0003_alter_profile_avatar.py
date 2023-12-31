# Generated by Django 4.0.6 on 2023-08-10 12:21

from django.db import migrations, models
import myauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0002_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=myauth.models.user_avatar_dir_path),
        ),
    ]
