# Generated by Django 5.0.1 on 2024-03-11 00:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umbrella', '0021_rent_is_disabled_alter_rent_return_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='return_due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 14, 0, 37, 57, 932264)),
        ),
    ]
