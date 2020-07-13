# Generated by Django 2.0.6 on 2020-07-06 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_auto_20200703_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='candidate',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Candidates', to='candidate.Candidate'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='client',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='clients', to='clients.Client'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='interview_round',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='InterviewRounds', to='interview.InterviewRound'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='interview_status',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='InterviewStatus', to='interview.InterviewStatus'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='job',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Jobs', to='clients.Job'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
