# Generated by Django 2.0.6 on 2020-06-23 13:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20200623_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(default=None, max_length=1024),
        ),
        migrations.AlterField(
            model_name='client',
            name='category',
            field=models.CharField(choices=[('PB', 'Public'), ('PR', 'Private'), ('OT', 'Other')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='ceo',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='founded_on',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='founder',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='headquarter',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='industry',
            field=models.CharField(choices=[('FN', 'Finance'), ('RS', 'Resources'), ('PD', 'Products'), ('HP', 'Health and public')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='latest_funding',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='mobile',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='profile_desc',
            field=models.CharField(default=None, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='revenue',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('on_hold', 'ON_HOLD'), ('expiried', 'EXPIRED')], default='active', max_length=256),
        ),
        migrations.AlterField(
            model_name='client',
            name='web_link',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
    ]
