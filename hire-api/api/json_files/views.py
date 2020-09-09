from django.shortcuts import render
from api.default_settings import MEDIA_ROOT,JSON_MEDIA_ROOT
from django.conf import settings
import json 
import os,io

from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Create your views here.


class JsonFileViewSet(GenericViewSet):

	"""
	user files
	"""

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def menu_sidebar(self, request):
		file=self.file_read('menu_sidebar.json')
		return file

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def user_designation(self, request):
		file=self.file_read('json_filesuser_designation.json')
		return file

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def user_columns(self, request):
		file=self.file_read('user_columns.json')
		return file
		

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def user_skills_dropdown(self, request):
		file=self.file_read('skills_dropdown.json')
		return file


	"""
	candidate files
	"""

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def candidate_skills_dropdown(self, request):
		file=self.file_read('skills_dropdown.json')
		return file



	@action(methods=['get', 'patch'],detail=False,
	  permission_classes=[],
	  )
	def candidate_prepared_location(self, request):
	  file=self.file_read('preffared_location.json')
	  return file


	@action(methods=['get', 'patch'],detail=False,
	  permission_classes=[],
	  )
	def candidate_columns(self, request):
		file=self.file_read('candidate_columns.json')
		return file

	"""
	client files
	"""

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def client_column_jsondata(self, request):

		file=self.file_read('client_columns.json')
		return file


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def client_category(self, request):

		file=self.file_read('category_response.json')
		return file
	

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def client_industry(self, request):

		file=self.file_read('industry_response.json')
		return file

	""" job files """

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def job_column_jsondata(self, request):

		file=self.file_read('job_columns.json')
		return file

	""" interview """

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def interview_columns(self, request):
		file=self.file_read('interview_columns.json')
		return file

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def interview_status(self, request):
		file=self.file_read('interview_status.json')
		return file
	

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def interview_round(self, request):
		file=self.file_read('interview_round.json')
		return file


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[],
		)
	def leave_management_columns(self, request):
		file=self.file_read('leave_management_columns.json')
		return file


	def file_read(self,file_name):
		file_path = os.path.join(JSON_MEDIA_ROOT,file_name)
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)