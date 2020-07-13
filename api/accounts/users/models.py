# python imports
import uuid

# django/rest_framwork imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator,MinValueValidator
# from django.core.validators import MinValueValidator
# from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
# from django.utils import timezone
# from django.conf import settings
from django.contrib.postgres.fields import JSONField

# project level imports
from libs.models import TimeStampedModel
# from libs.clients import sms_client
# from libs.utils.otp import create_otp
import django.utils.datetime_safe

# app level imports
from .managers import UserManager
# from accounts.constants import TOO_MANY_ATTEMPTS, INVALID_OTP
# from accounts.models import Actions,Permissions,UserPermissions

# third party imports
from model_utils import Choices
from django.db.models import CharField



class UserRole(TimeStampedModel):
	"""
	"""
	
	ROLE = Choices(

		('executive', 'EXECUTIVE'),
		('manager', 'MANAGER'),
		('admin', 'ADMIN'),
	)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	role_name = models.CharField(
		max_length=256,
		choices=ROLE,
		default=ROLE.executive
	)
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
		app_label = 'accounts'
		db_table = 'api_user_role'


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
	"""
	User model represents the user data in the database.
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

	first_name= models.CharField(max_length=64, blank=False,default=None)
	last_name=models.CharField(max_length=64,null=True,blank=True)
	email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False,default=None)
	mobile =models.BigIntegerField(
		validators=[
			MinValueValidator(5000000000),
			MaxValueValidator(9999999999),
		],
		unique=True,
		db_index=True,default=None,blank=False)
	dob= models.DateField(null=True,blank=True)
	gender=models.CharField(choices=GENDER, max_length=10,null = True, blank=True, default=GENDER.M)
	address=models.CharField(max_length=64, blank=True,null = True,default=None)
	qualification=models.CharField(max_length=64, blank=False,default=None)
	specialization=models.CharField(max_length=64,null = True, blank=True,default=None)
	marks=models.CharField(max_length=64, blank=True,null = True,default=None)
	passing_year=models.CharField(max_length=64, blank=True,null = True,default=None)
	college=models.CharField(max_length=64, blank=True,null = True,default=None)
	work_experience=models.CharField(max_length=64,null = True, blank=True)
	skills=JSONField(default={}, blank=True, null=True)
	designation=models.CharField(max_length=64,null = True, blank=True)
	anual_salary=models.CharField(max_length=64,null = True, blank=True)
	work_location=models.CharField(max_length=64,null = True, blank=True)
	previous_company=models.CharField(max_length=64,null = True, blank=True)
	status= models.CharField(max_length=64, choices=STATUS,blank=True, default=STATUS.active)

	profile_pic= models.ImageField(max_length=255,null=True, blank=True)
	joined_date= models.DateField(null=True,blank=True)
	resigned_date= models.DateField(null=True,blank=True)
	exit_date= models.DateField(null=True,blank=True)
	reporting_to=models.CharField(max_length=64, null=True,blank=True)











	# id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	# email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
	# mobile = models.BigIntegerField(
	# 	validators=[
	# 		MinValueValidator(5000000000),
	# 		MaxValueValidator(9999999999),
	# 	],
	# 	unique=True,
	# 	db_index=True,)
	# employee_id = models.CharField(max_length=255, blank=False, default=uuid.uuid4)

	# reporting_manager = models.CharField(max_length=64, blank=True)
	# first_name = models.CharField(max_length=64, blank=True)
	# last_name = models.CharField(max_length=64, blank=True)
	# gender = models.CharField(choices=GENDER, max_length=1, blank=False, default=GENDER.M)
	# role = models.ForeignKey(
	# 	UserRole,
	# 	on_delete=models.PROTECT,
	# 	related_name='role',
	# 	blank=True,
	# 	null=True
	# )

	# image_url = models.ImageField(max_length=255, blank=False)

	# login_attempts_count = models.IntegerField(default=0)
	# is_blocked = models.BooleanField(default=False)
	# block_reason = models.CharField(max_length=255, blank=True)
	# is_active = models.BooleanField(default=True)
	# is_staff = models.BooleanField(default=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['mobile']

	class Meta:
		app_label = 'accounts'
		db_table = 'api_user'

	def __str__(self):
		# print("printing object")
		return str(self.mobile)

	@property
	def access_token(self):
		token, is_created = Token.objects.get_or_create(user=self)
		return token.key

	@property
	def full_name(self):
		return "{fn} {ln}".format(fn=self.first_name, ln=self.last_name)

	@property
	def user_groups(self):
		return self.groups.values_list('name', flat=True)

	def save(self, *args, **kwargs):
		"""
		if has_django_dashboard_access is True, then setting is_staff to True
		"""

		# if self.has_django_dashboard_access is True:
		#     self.is_staff = True
		super(User, self).save(*args, **kwargs)



class Permissions(TimeStampedModel):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
	permissions = CharField(max_length=256,blank=True, null=True)
	discription=CharField(max_length=256,blank=True,null=True)



class Actions(TimeStampedModel):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	action_name=models.CharField(max_length=256,blank=True, null=True)



class UserPermissions(TimeStampedModel):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	actions=models.ForeignKey(
		Actions,on_delete=models.PROTECT,
		related_name='actions',blank=True,null=True
		)
	user = models.ForeignKey(
		User,on_delete=models.PROTECT,blank=True,null=True
		)
	permission=models.ForeignKey(Permissions,
		on_delete=models.PROTECT,related_name='permission',
		blank=True,null=True
		)