# Generated by Django 5.0.1 on 2024-02-11 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_studentcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='studentCard',
            field=models.ImageField(upload_to='profile'),
        ),
    ]