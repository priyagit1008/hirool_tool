# Generated by Django 2.0.6 on 2020-07-09 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management', '0005_auto_20200709_1213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leavetracker',
            old_name='discription',
            new_name='description',
        ),
    ]