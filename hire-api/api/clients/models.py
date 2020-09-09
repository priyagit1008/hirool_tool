# django imports
from django.db import models
from django.contrib.postgres.fields import JSONField
# import datetime
import uuid

# project level imports
from libs.models import TimeStampedModel

# third party imports
from model_utils import Choices


from datetime import timedelta
from django.utils import timezone


def one_month_from_today():
    return timezone.now() + timedelta(days=30)



    
class Client(TimeStampedModel):
    """
    """

    CLIENT_INDUSTRY= Choices(
        ('Finance','FINANCE'),
        ('Resources','RESOURCES'),
        ('Products','PRODUCTS'),
        ('Health and public','HEALTH AND PUBLIC'),
        )

    CLIENT_CATEGORY = Choices(
        ('Public','PUBLIC'),
        ('Private','PRIVATE'),
        ('Other','OTHER')
        )

    STATUS = Choices(
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
        ('on_hold', 'ON_HOLD'),
        ('expiried', 'EXPIRED'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,blank=False)
    name = models.CharField(max_length=512,unique=True, db_index=True,blank=False)
    web_link = models.CharField(max_length=512,blank=False)
    ceo=models.CharField(max_length=512, null = True, blank=True)
    founder=models.CharField(max_length=512,null = True,blank=True)
    founded_on=models.CharField(max_length=512, null = True,blank=True)
    email=models.CharField(max_length=512, blank=False)
    mobile=models.CharField(max_length=512, blank=False)
    revenue=models.CharField(max_length=512, null = True, blank=True)
    latest_funding=models.CharField(max_length=512, null = True,blank=True)
    headquarter = models.CharField(max_length=512,null = True,  blank=True)
    address = models.CharField(max_length=1024,null = True, blank=True)
    profile_desc = models.CharField(max_length=1024, null = True,blank=True)
    aggrement_doc = models.CharField(max_length=1024, null = True,blank=True)
    status = models.CharField(max_length=256,null = True, choices=STATUS, default=STATUS.active)
    industry=models.CharField(max_length=200,null = True, choices=CLIENT_INDUSTRY,default=CLIENT_INDUSTRY.Products)
    category=models.CharField(max_length=200,null = True, choices=CLIENT_CATEGORY,default=CLIENT_CATEGORY.Private)
    def __str__(self):
        return "{id}".format(id=self.id)



    class Meta:
        app_label = 'clients'
        db_table = 'api_client'
