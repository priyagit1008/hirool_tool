# Generated by Django 2.0.6 on 2020-01-23 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0012_auto_20200123_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='certification',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]