# Generated by Django 5.0.1 on 2024-02-05 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='studentID',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
