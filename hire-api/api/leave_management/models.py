import uuid
from django.db import models
from libs.models import TimeStampedModel
from accounts.models import User

from model_utils import Choices
from django.contrib.postgres.fields import JSONField


class LeaveType(TimeStampedModel):
	LEAVE_TYPE = Choices(
		('Planned', 'PLANNED'),
		('Emergancy', 'EMERGANCY'),
		('Sick', 'SICK'),
	)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	leave_type = models.CharField(max_length=256, choices=LEAVE_TYPE, default=LEAVE_TYPE.Planned) 

	class Meta:
		app_label = 'leave_management'
		db_table = 'api_leave_type'
	

	
class  LeaveTracker(TimeStampedModel):
	LEAVE_STATUS = Choices(
		('Pending', ' PENDING'),
		('Approved', 'APPROVED'),
		('Rejected','REJECTED'),
	)
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	user = models.ForeignKey(User,on_delete=models.PROTECT)
	leave_type = models.ForeignKey(LeaveType,on_delete=models.PROTECT)
	leave_status = models.CharField(max_length=256, choices=LEAVE_STATUS,default=LEAVE_STATUS.Pending)
	from_date = models.DateField(blank=False)
	applied_date=models.DateField(auto_now_add=True,null=True)
	to_date = models.DateField(blank=False)
	approved_date =models.DateField(blank=True,null=True)
	total_leaves = models.IntegerField(default=30)
	available_leaves = models.IntegerField(default=30,null=True,blank=False)
	description = models.CharField(max_length=250,blank=True)
	approved_by = models.ForeignKey(User,on_delete=models.PROTECT,related_name = 'approved_by',null=True,blank=True)



	# @property
 #    def date_diff(self):
 #        return (self.to_date - self.from_date).days

	class Meta:
		app_label = 'leave_management'
		db_table = 'api_tracker'



