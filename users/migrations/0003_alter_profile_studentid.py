# Generated by Django 5.0.1 on 2024-02-05 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_studentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='studentID',
            field=models.IntegerField(default=0),
        ),
    ]