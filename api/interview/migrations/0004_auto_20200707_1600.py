# Generated by Django 2.0.6 on 2020-07-07 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0003_auto_20200706_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='interview_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='InterviewStatus', to='interview.InterviewStatus'),
        ),
    ]
