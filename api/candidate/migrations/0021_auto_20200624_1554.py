# Generated by Django 2.0.6 on 2020-06-24 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0020_auto_20200624_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='dob',
            field=models.DateField(null=True),
        ),
    ]