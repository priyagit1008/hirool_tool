# Generated by Django 2.0.6 on 2020-01-23 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0011_candidate_certification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='certification',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
    ]