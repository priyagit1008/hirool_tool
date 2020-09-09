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
from clients.models import Client
from accounts.models import User
from candidate.models import Candidate
from jobs.models import Job

# third party imports
from model_utils import Choices

class InterviewRound(TimeStampedModel):
	"""docstring for Role"""
	INTERVIEW_ROUND= Choices(
		('Online round','ONLINE ROUND'),
		('Technical round','TECHNICAL ROUND'),
		('HR round','HR ROUND'),
		)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	interview_round=models.CharField(max_length=200,choices=INTERVIEW_ROUND)

	

class InterviewStatus(TimeStampedModel):
	"""docstring for Status"""
	STATUS = Choices(
		('Processing','PROCESSING'),
		('Completed','COMPLETED'),
		('Sheduled','SHEDULED'),
	)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	status = models.CharField(max_length=256, choices=STATUS, default=STATUS.Processing) 

	

class Interview(TimeStampedModel):
	"""docstring for Interview"""
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,blank=False)

	client= models.ForeignKey(Client,
		on_delete=models.PROTECT,
		related_name='clients',null=True,blank=False)

	job = models.ForeignKey(Job,on_delete=models.PROTECT,
		related_name='Jobs',
		blank=False,null=True)

	interview_round= models.ForeignKey(InterviewRound,on_delete=models.PROTECT,
		related_name='InterviewRounds',
		blank=False,null=True)

	candidate= models.ForeignKey(Candidate,on_delete=models.PROTECT,
		related_name='Candidates',
		blank=False,null=True)

	user= models.ForeignKey(User,on_delete=models.PROTECT,
		related_name='accounts',
		blank=False,null=True)

	date = models.DateField()

	location = models.CharField(max_length=256,blank=False,null=False)

	interview_status= models.ForeignKey(InterviewStatus,on_delete=models.PROTECT,
		related_name='InterviewStatus',
		blank=True,null=True)



	class Meta:
		app_label = 'interview'
		db_table = 'api_interview'

