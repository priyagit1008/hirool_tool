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


def user_directory_path(instance, filename): 
  
      extension  = filename.split(".")[-1]
      # return 'user_%S/%s'.format(instance.id,filename)
      # extension = filename[0-5]
      return 'user_{0}/{1}.{2}'.format("images",instance.first_name,extension) 
 


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
      """
      User model represents the user data in the database.
      """
      STATUS = Choices(
            ('active','ACTIVE' ),
            ('inactive','INACTIVE'),
      )

      GENDER = Choices(
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
      )
      id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

      first_name= models.CharField(max_length=64, blank=False)
      last_name=models.CharField(max_length=64,null=True,blank=True)
      email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
      mobile =models.BigIntegerField(
            validators=[
                  MinValueValidator(5000000000),
                  MaxValueValidator(9999999999),
            ],
            unique=True,
            db_index=True,blank=False)
      dob= models.DateField(null=True,blank=True)
      gender=models.CharField(choices=GENDER, max_length=10,null = True, blank=True)
      address=models.CharField(max_length=64, blank=True,null = True)
      qualification=models.CharField(max_length=64, blank=False)
      specialization=models.CharField(max_length=64,null = True, blank=True)
      marks=models.CharField(max_length=64, blank=True,null = True)
      passing_year=models.CharField(max_length=64, blank=True,null = True)
      college=models.CharField(max_length=64, blank=True,null = True)
      work_experience=models.CharField(max_length=64,null = True, blank=True)
      skills=CharField(max_length=100,blank=True, null=True)
      designation=models.CharField(max_length=64,null = True, blank=True)
      anual_salary=models.CharField(max_length=64,null = True, blank=True)
      work_location=models.CharField(max_length=64,null = True, blank=True)
      previous_company=models.CharField(max_length=64,null = True, blank=True)
      status= models.CharField(max_length=64, choices=STATUS,blank=True, default=STATUS.active)

      image_url= models.ImageField(upload_to = user_directory_path,max_length=255,null=True, blank=True)
      joined_date= models.DateField(null=True,blank=True)
      resigned_date= models.DateField(null=True,blank=True)
      exit_date= models.DateField(null=True,blank=True)
      reporting_to=models.CharField(max_length=64, null=True,blank=True)


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