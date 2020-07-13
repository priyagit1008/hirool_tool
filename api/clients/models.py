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
        ('FN','Finance'),
        ('RS','Resources'),
        ('PD','Products'),
        ('HP','Health and public'),
        )

    CLIENT_CATEGORY = Choices(
        ('PB','Public'),
        ('PR','Private'),
        ('OT','Other')
        )

    STATUS = Choices(
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
        ('on_hold', 'ON_HOLD'),
        ('expiried', 'EXPIRED'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,blank=False)
    name = models.CharField(max_length=512,unique=True, db_index=True, default=None,blank=False)
    web_link = models.CharField(max_length=512, default=None, blank=False)
    ceo=models.CharField(max_length=512, null = True, blank=True)
    founder=models.CharField(max_length=512,null = True, default=None,blank=True)
    founded_on=models.CharField(max_length=512, null = True,default=None,blank=True)
    email=models.CharField(max_length=512, blank=False)
    mobile=models.CharField(max_length=512, blank=False)
    revenue=models.CharField(max_length=512, null = True, blank=True)
    latest_funding=models.CharField(max_length=512, null = True,blank=True)
    headquarter = models.CharField(max_length=512,null = True,  blank=True)
    address = models.CharField(max_length=1024,null = True, blank=True)
    profile_desc = models.CharField(max_length=1024, null = True,blank=True)
    aggrement_doc = models.CharField(max_length=1024, null = True,blank=True)
    status = models.CharField(max_length=256,null = True, choices=STATUS, default=STATUS.active)
    industry=models.CharField(max_length=200,null = True, blank=True, choices=CLIENT_INDUSTRY)
    category=models.CharField(max_length=200,null = True, blank=True, choices=CLIENT_CATEGORY,default=CLIENT_CATEGORY.PR)
    def __str__(self):
        return "{id}".format(id=self.id)


    def modify(self, payload):
        """
        This method will update tasks attributes
        """
        for key, value in payload.items():
            setattr(self, key, value)
        self.save()

    class Meta:
        app_label = 'clients'
        db_table = 'api_client'


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
    job_title = models.CharField(max_length=512, default=None, blank=False)
    jd_url = models.CharField(max_length=1024, default=None,null=True, blank=True)
    tech_skills = JSONField(default={}, blank=True, null=True)
    job_location = models.CharField(max_length=512, default=None, null=True, blank=True)
    job_type = models.CharField(max_length=256, choices=JOB_TYPE, default=JOB_TYPE.permanent)
    min_exp = models.IntegerField(default=0,null=True,blank=True)  # number of years
    max_exp = models.IntegerField(default=60,null=True,blank=True)  # number of years # number of years
    min_notice_period = models.IntegerField(default=60,null=True,blank=True)  # number of days
    max_notice_period =  models.IntegerField(default=90,null=True,blank=True)
    # role = models.CharField(max_length=512, default=None, null=True, blank=True)
    min_ctc = models.FloatField(default=0.0,null=True,blank=True)  # LPA
    max_ctc = models.FloatField(default=1000.0,null=True,blank=True)  # LPA
    qualification=models.CharField(max_length=100,blank=True,null=True,default=None)
    percentage_criteria=models.CharField(max_length=100,null=True,blank=True,default=None)
    status = models.CharField(max_length=256, choices=STATUS, default=STATUS.active)
    # May have Salary breakup, facilities, any other data
    jd_extra = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return "{id}".format(id=self.id)

    def modify(self, payload):
        """
        This method will update tasks attributes
        """
        for key, value in payload.items():
            setattr(self, key, value)
        self.save()

    class Meta:
        app_label = 'clients'
        db_table = 'api_jobs'
