# Generated by Django 5.0.2 on 2024-03-30 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('companies', '0001_initial'),
        ('jobs', '0001_initial'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.category'),
        ),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.company'),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.location'),
        ),
    ]
