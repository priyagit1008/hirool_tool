# Generated by Django 2.0.6 on 2020-06-26 09:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20200626_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=512, null=True, validators=[django.core.validators.MinValueValidator(2)]),
        ),
    ]