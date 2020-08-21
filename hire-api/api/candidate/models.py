from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField

# project level imports
from libs.models import TimeStampedModel
# import datetime
import uuid
from django.contrib.auth.models import UserManager

# third party imports
from model_utils import Choices

from datetime import timedelta
from django.utils import timezone


# Create your models here.

def user_directory_path(instance, filename): 
  
	extension  = filename.split(".")[-1]
	# return 'user_%S/%s'.format(instance.id,filename)
	# extension = filename[0-5]
	return 'user_{0}/{1}.{2}'.format("resumes",instance.id,extension) 



class Candidate(TimeStampedModel):
	"""
	"""
	STATUS = Choices(
		('active', 'ACTIVE'),
		('inactive', 'INACTIVE'),
	)
	GENDER = Choices(
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Other'),
	)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name=models.CharField(max_length=512,null= True,blank=False)
	last_name=models.CharField(max_length=512,null= True,blank=True)
	email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
	candidate_url = models.CharField(max_length=1024, default=None, null = True, blank=True)
	mobile = models.BigIntegerField(
		validators=[
			MinValueValidator(5000000000),
			MaxValueValidator(9999999999),
		],
		unique=True,
		db_index=True,)
	dob=models.DateField(null=True)
	gender=models.CharField(choices=GENDER, max_length=6,null = True, blank=True, default=GENDER.M)
	sslc_marks=models.CharField(max_length=100,blank=True,null = True,default=None)
	puc_marks=models.CharField(max_length=100,blank=True,null = True,default=None)
	bachelor_degree = models.CharField(max_length=100,blank=True,null = True,default=None)
	bachelor_degree_course=models.CharField(max_length=100,blank=True,null = True,default=None)
	bachelor_degree_marks=models.CharField(max_length=100,blank=True,null = True,default=None)
	master_degree=models.CharField(max_length=100,blank=True,null = True,default=None)
	master_degree_course=models.CharField(max_length=100,blank=True,null = True,default=None)
	master_degree_marks=models.CharField(max_length=100,blank=True,null = True,default=None)
	address=models.CharField(max_length=1024, default=None, null=True, blank=True)
	tech_skills=models.CharField(max_length=100,blank=True, null=True)
	prefered_location=JSONField(default={},max_length=100,null = True,blank=True)
	previous_company=models.CharField(max_length=100,blank=True,null = True,default=None)
	work_experience=models.FloatField(max_length=100,blank=True,null = True,default=None)
	current_ctc=models.FloatField(default=0.0,null = True,blank=True,)
	expected_ctc=models.FloatField(default=1000.0,null = True,blank=True)
	notice_period=models.IntegerField(default=60,null = True,blank=True)
	resume= models.FileField(upload_to = user_directory_path,blank=True,null = True)
	status=models.CharField(max_length=256,blank=True, choices=STATUS, default=STATUS.active)

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
		app_label = 'candidate'
		db_table = 'api_candidate'

	# @property
 #    def full_name(self):
 #        return "{fn} {ln}".format(fn=self.first_name, ln=self.last_name)