# Generated by Django 2.0.6 on 2020-07-09 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management', '0003_leavetracker_applied_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavetype',
            name='available_leaves',
        ),
        migrations.AddField(
            model_name='leavetracker',
            name='available_leaves',
            field=models.IntegerField(null=True),
        ),
    ]
