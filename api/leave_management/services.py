import json
from django.core import serializers
from .models import LeaveType,LeaveTracker
class LeaveTrackerServices:

	def leave_filter_service(self,filter_data):
		return LeaveTracker.objects.filter(**filter_data)
		
	def get_leave_service(self,id):
		return LeaveTracker.objects.get(id = id)

	def update_leave_service(self,id):
		return LeaveTracker.objects.get(id = id)



		
class LeaveType_Services:

	def LeaveType_filter_service(self,filter_data):
		return LeaveType.objects.filter(**filter_data)
	def get_leavetype_service(self,id):
		return LeaveType.objects.get(id=id)




# class LeaveStatus_Services:
# 	def LeaveStatus_filter_service(self,filter_data):
# 		return LeaveStatus.objects.filter(**filter_data)

# 	def get_leavestatus_service(self,id):
# 		return LeaveStatus.objects.get(id=id)
		



# class Client_get_Service:
# 	def get_service(self,id):
# 		clients_get=Client.objects.get(id=id)


			