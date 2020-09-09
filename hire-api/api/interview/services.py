from .models import Interview,InterviewRound,InterviewStatus
import json
from django.core import serializers
from clients.models import Client
from jobs.models import Job

from accounts.models import User
from candidate.models import Candidate

class InterviewServices:

	def interview_filter_service(self,filter_data):
		return Interview.objects.filter(**filter_data)
		
	def get_interview_service(self,id):
		return Interview.objects.get(id = id)

	def update_interview_service(self,id):
		return Interview.objects.get(id = id)



		
class InterviewRound_Services:

	def interviewround_filter_service(self,filter_data):
		return InterviewRound.objects.filter(**filter_data)
	def get_Round_service(self,id):
		return InterviewRound.objects.get(id=id)




class InterviewStatus_Services:
	def interviewstatus_filter_service(self,filter_data):
		return InterviewStatus.objects.filter(**filter_data)

	def get_status_service(self,id):
		return InterviewStatus.objects.get(id=id)
		



# class Client_get_Service:
# 	def get_service(self,id):
# 		clients_get=Client.objects.get(id=id)


			