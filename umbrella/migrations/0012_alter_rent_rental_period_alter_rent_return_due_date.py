# Generated by Django 5.0.1 on 2024-02-10 19:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umbrella', '0011_rent_rental_period_alter_rent_return_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='rental_period',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rent',
            name='return_due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 13, 19, 27, 27, 997532)),
        ),
    ]
