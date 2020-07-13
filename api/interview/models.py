from django.db import models

# Create your models here.

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField
# project level imports
from libs.models import TimeStampedModel
# import datetime
import uuid
# from .models import InterviewRound
# from .models import InterviewStatus
from clients.models import Client,Job
from accounts.models import User
from candidate.models import Candidate

# third party imports
from model_utils import Choices

class InterviewRound(TimeStampedModel):
	"""docstring for Role"""
	INTERVIEW_ROUND= Choices(
		('FR','Online round'),
		('SR','Technical round'),
		('TR','HR round'),
		)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	interview_round=models.CharField(max_length=200,choices=INTERVIEW_ROUND)

class InterviewStatus(TimeStampedModel):
	"""docstring for Status"""
	STATUS = Choices(
		('FS','Processing'),
		('SS','Completed'),
		('TS','Sheduled'),
	)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	status = models.CharField(max_length=256, choices=STATUS, default=STATUS.FS)   

class Interview(TimeStampedModel):
	"""docstring for Interview"""
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,blank=False)
	# client_id = models.ForeignKey(Client,on_delete=models.PROTECT,related_name='client_id',blank=False,default=None)
	client= models.ForeignKey(Client,
        on_delete=models.PROTECT,
        related_name='clients',null=True,blank=False,default=None)

	job = models.ForeignKey(Job,on_delete=models.PROTECT,
		related_name='Jobs',
		blank=False,null=True,default=None)

	interview_round= models.ForeignKey(InterviewRound,on_delete=models.PROTECT,
		related_name='InterviewRounds',
		blank=False,null=True,default=None)

	candidate= models.ForeignKey(Candidate,on_delete=models.PROTECT,
		related_name='Candidates',
		blank=False,null=True,default=None)

	user= models.ForeignKey(User,on_delete=models.PROTECT,
		related_name='accounts',
		blank=False,null=True,default=None)

	date = models.DateField()
	location = models.CharField(max_length=256,blank=False,null=False,default=None)

	interview_status= models.ForeignKey(InterviewStatus,on_delete=models.PROTECT,
		related_name='InterviewStatus',
		blank=True,null=True)
	# status = models.CharField(max_length=256, choices=STATUS, default=STATUS.active)


