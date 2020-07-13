# app levelimports
from rest_framework import serializers
import json

from .models import Candidate

class CandidateServices:



	def get_queryset_service(self,filter_data):
		return Candidate.objects.filter(**filter_data)

	def get_candidate_service(self,id):
		return Candidate.objects.get(id = id)

	def update_candidate_service(self,id):
		return Candidate.objects.get(id = id)
	