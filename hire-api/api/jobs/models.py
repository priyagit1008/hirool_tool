from django.db import models


from django.db import models
from django.contrib.postgres.fields import JSONField
# import datetime
import uuid

# project level imports
from libs.models import TimeStampedModel

# third party imports
from clients.models import Client

from model_utils import Choices


from datetime import timedelta
from django.utils import timezone

# Create your models here.




class Job(TimeStampedModel):
    """
    The JD table
    """

    STATUS = Choices(
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
        ('on_hold', 'ON_HOLD'),
        ('expiried', 'EXPIRED'),
    )

    JOB_TYPE = Choices(
        ('permanent', 'PERMANENT'),
        ('contract', 'CONTRACT'),
        ('part_time', 'PART_TIME'),
    )
    client = models.ForeignKey(
        Client, blank=False,
        on_delete=models.PROTECT,
        related_name='client'
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_title = models.CharField(max_length=512,blank=False)
    jd_url = models.CharField(max_length=1024,null=True, blank=True)
    tech_skills = JSONField(default={}, blank=True, null=True)
    job_location = models.CharField(max_length=512,null=True, blank=True)
    job_type = models.CharField(max_length=256, choices=JOB_TYPE, default=JOB_TYPE.permanent)
    min_exp = models.IntegerField(default=0,null=True,blank=True)  # number of years
    max_exp = models.IntegerField(default=60,null=True,blank=True)  # number of years 
    min_notice_period = models.IntegerField(default=60,null=True,blank=True)  # number of days
    max_notice_period =  models.IntegerField(default=90,null=True,blank=True)
    # role = models.CharField(max_length=512, default=None, null=True, blank=True)
    min_ctc = models.FloatField(null=True,blank=True)  # LPA
    max_ctc = models.FloatField(null=True,blank=True)  # LPA
    qualification=models.CharField(max_length=100,blank=True,null=True)
    percentage_criteria=models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=256, choices=STATUS, default=STATUS.active)
    # May have Salary breakup, facilities, any other data
    jd_extra = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return "{id}".format(id=self.id)
