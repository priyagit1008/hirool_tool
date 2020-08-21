# django imports

import unicodedata
import os,io
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
import fileinput 

import json 
import requests
import csv

from django.core.paginator import Paginator
from django.core.files import File
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Candidate
from django.db import models



# app level imports

from accounts.users.permissions import HiroolReadOnly,HiroolReadWrite
from .serializers import (
	CandidateCreateRequestSerializer,
	CandidateListSerializer,
	CandidateListSerializer,
	CandidateUpdateSerializer,
	CandidateSkillsDrowpdownGetSerializer,
	)
from .services import CandidateServices
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
		
)
from libs.pagination import StandardResultsSetPagination

from libs import (
				# redis_client,
				otpgenerate,
				mail,
				)
from api.default_settings import MEDIA_ROOT,JSON_MEDIA_ROOT

from libs.exceptions import ParseException
import codecs 


# Create your views here.

class CandidateViewSet(GenericViewSet):
	"""docstring for candidateViewset"""
	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = CandidateServices()
	queryset=Candidate.objects.all().order_by('-created_at')
	pagination_class = StandardResultsSetPagination



	filter_backends = (filters.OrderingFilter,)
	parser_class = (FileUploadParser,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict={
			'candidate_Registration':CandidateCreateRequestSerializer,
			'candidate_list':CandidateListSerializer,
			'candidate_get':CandidateListSerializer,
			'candidate_update':CandidateUpdateSerializer,
			'candidate_skills_dropdown':CandidateSkillsDrowpdownGetSerializer,
			}


	def get_queryset(self,filterdata=None):
		if filterdata:
			self.queryset =Candidate.objects.filter(**filterdata)
		return self.queryset

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,],)
	def candidate_Registration(self,request):
		"""
		Returns candidate account creation
		"""
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():

			raise ParseException({'status':'Incorrect Input'}, serializer.errors)

		if Candidate.objects.filter(email=self.request.data['email']).exists():
			return Response({"status":"candidate already exists"},status=status.HTTP_400_BAD_REQUEST)

		print("create candidate with", serializer.validated_data)
		candidate= serializer.create(serializer.validated_data)

		if candidate:

			msg_plain = render_to_string('email_message.txt',{"user":candidate.first_name})
			msg_html = render_to_string('email.html',{"user":candidate.first_name})
			send_mail('Hirool',msg_plain,settings.EMAIL_HOST_USER,[candidate.email],html_message=msg_html,)

			return Response({'status':'Successfully added'},status=status.HTTP_201_CREATED)
		return Response({"status": "Not Found"},status.HTTP_404_NOT_FOUND) 


	def candidate_query_string(self,filterdata):
		dictionary={}
			 
		if "prefered_location" in filterdata:
			dictionary["prefered_location__icontains"] = filterdata.pop("prefered_location")

		if "tech_skills" in filterdata:
			dictionary["tech_skills__icontains"] = filterdata.pop("tech_skills")


		if "work_experience_from" in filterdata:
			dictionary["work_experience__gte"] = filterdata.pop("work_experience_from")

		if "work_experience_to" in filterdata:
			dictionary["work_experience__lte"] = filterdata.pop("work_experience_to")
		if "current_ctc" in filterdata:
			dictionary["current_ctc__gte"] = filterdata.pop("current_ctc")
		if "expected_ctc" in filterdata:
			dictionary["expected_ctc__lte"] = filterdata.pop("expected_ctc")
		if "notice_period_from" in filterdata:
			dictionary["notice_period__gte"] = filterdata.pop("notice_period_from")
		if "notice_period_to" in filterdata:
			dictionary["notice_period__lte"] = filterdata.pop("notice_period_to")




		if "prefered_location" in filterdata:
			filterdata["prefered_location__icontains"] = filterdata.pop("prefered_location")

		if "tech_skills" in filterdata:
			filterdata["tech_skills__icontains"] = filterdata.pop("tech_skills")

		if "work_experience_from" in filterdata:
			filterdata["work_experience__gte"] = filterdata.pop("work_experience_from")

		if "work_experience_to" in filterdata:
			filterdata["work_experience__lte"] = filterdata.pop("work_experience_to")

		if "current_ctc" in filterdata:
			filterdata["current_ctc__gte"] = filterdata.pop("current_ctc")

		if "expected_ctc" in filterdata:
			filterdata["expected_ctc__lte"] = filterdata.pop("expected_ctc")

		if "notice_period_from" in filterdata:
			filterdata["notice_period__gte"]  = filterdata.pop("notice_period_from")

		if "notice_period_to" in filterdata:
			filterdata["notice_period__lte"]  = filterdata.pop("notice_period_to")
		
		return dictionary

		
	
	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def candidate_list(self,request,**dict):
		"""
		Returns candidate list
		"""
		try:
			filterdata = self.candidate_query_string(request.query_params.dict())
			# page_result = self.candidate_query_set(filterdata)
			page = self.paginate_queryset(self.get_queryset(filterdata))
			serializer = self.get_serializer(page,many=True)

			return self.get_paginated_response(serializer.data)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def candidate_get(self,request):
		"""
		Returns single candidate details
		"""
		id= request.GET.get('id', None)
		if not id:
				return Response({"status": False, "message":"id is required"})
		try:
			serializer = self.get_serializer(self.services.get_candidate_service(id))
		except Candidate.DoesNotExist:
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
		return Response(serializer.data, status.HTTP_200_OK)




	@action(methods=['get','put'],detail=False,permission_classes=[IsAuthenticated,],)
	def candidate_update(self,request):
		"""
		update candidate details
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_candidate_service(id),data=request.data)
			if not serializer.is_valid():
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()    
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def candidate_skills_dropdown(self,request):
		"""
		Returns single candidate details
		"""
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.get_queryset_service(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(
		methods=['get'],
		detail= False,
		permission_classes=[IsAuthenticated,],
		)
	def resume_download(self,request, encoding='utf-8'):
		"""
		Download candidate resume
		"""
		try:
			candidate_id=request.GET["id"]
			resume_name = Candidate.objects.get(id=candidate_id).resume
			resume_path = os.path.join(MEDIA_ROOT,str(resume_name))
			FilePointer = open(resume_path,'rb')
			response = HttpResponse((FilePointer),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
			response['Content-Disposition'] = 'attachment; filename="%s.docx"' %(resume_name)

			return response
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def candidate_columns(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('candidate_columns.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def candidate_skills_dropdown(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('skills_dropdown.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)
		# myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/skills_dropdown.json','r')
		

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def candidate_prepared_location(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('prepared_location.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)

	
	@action(
		methods=['get'],
		detail=False,permission_classes=[],
	)
	def candidate_send_email(self,request,**dict):
		"""
		send mail api
		"""
		try:
			msg_plain = render_to_string('email_message.txt',{"user":candidate.email})
			msg_html = render_to_string('email.html',{"user":candidate.email})
			mail.sendmail.delay(msg_plain,"hi",[request.user.email])
			send_mail('Hirool',msg_plain,settings.EMAIL_HOST_USER,[candidate.email],html_message=msg_html)
			return Response("hi")
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)



	@action(
		methods=['get'],
		detail= False,
		permission_classes=[IsAuthenticated,],
		)
	def candidate_bulk_file_format(self,request, encoding='utf-8'):
		"""
		Download candidate resume
		"""
		try:
			file_path = os.path.join(MEDIA_ROOT,str('sample.csv'))
			FilePointer = open(file_path,'r')
			response = HttpResponse((FilePointer),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
			response['Content-Disposition'] = 'attachment; filename="%s"' %('sample.csv')

			return response
		except Exception as e:
			
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(
		methods=['get'],
		detail=False,permission_classes=[],
	)
	def candidate_bulk_uplode(self,request):
		# fileForInput = open('sample.csv','r')
		# print(request.object)
		f=request.FILES['file']
		file = f.read().decode('utf-8').splitlines()

		try:
			dr=csv.DictReader(file)
			cand=Candidate()
			candidates=[]
			for row in dr:
				candidate_obj=Candidate(**row)
				try:
					candidate_obj.full_clean()
				except ValidationError:
					continue
				candidates.append(candidate_obj)

			d1=(len(candidates))
			data=Candidate.objects.bulk_create(candidates)
			return Response({"status":"Successfully inserted","total candidates":d1},status=status.HTTP_201_CREATED)
		except Exception as e:

			return Response({"status":str(e)},status.HTTP_404_NOT_FOUND)



		# try:
		# 	with open('/home/priya/workspace/hire-api/api/libs/json_files/sample.csv','r') as file:
		# 		dr=csv.DictReader(file)
		# 		cand=Candidate()
		# 		candidates=[]
		# 		for row in dr:
		# 			print(row)
		# 			candidate_obj=Candidate(**row)
		# 			try:
		# 				candidate_obj.full_clean()
		# 			except ValidationError:
		# 				continue
		# 			candidates.append(candidate_obj)
		# 		data=Candidate.objects.bulk_create(candidates)
		# 		return Response({"status":"Successfully inserted"},status=status.HTTP_201_CREATED)
		# except Exception as e:
		# 	raise
		# 	return Response({"status":str(e)},status.HTTP_404_NOT_FOUND)








#------------------------------------**************************************------------------------------------------------------------------------------------#

		# with open('/home/priya/workspace/hire-api/api/libs/json_files/sample.csv','r') as f:
		# 	try:
		# 		dire=csv.reader(f)
		# 		cd=[]
		# 		for row in dire:
		# 			print(row)
		# 		return Response({"status":"Successfully inserted"},status=status.HTTP_201_CREATED)
		# 	except Exception as e:
		# 		raise
		# 		return Response({"status":str(e)},status.HTTP_404_NOT_FOUND)


			# with open('/home/priya/workspace/hire-api/api/libs/json_files/sample.csv','r') as file:

			# license = SubscriptionLicense(
   #      )




				# candidate=Candidate(**row)
				# data=Candidate.objects.bullk_create(list)
				

 
  #       for row in reader:
  #           city = City(**row)
  #           print(city)
		# try:
		#   with open('/home/priya/workspace/hire-api/api/libs/json_files/sample.csv','r') as file:
		#       dr=csv.DictReader(file)
		#       print(dr)
		#       list=[]
		#       user=(**user)
		#       user.full_clean()
		#       user.append(list)
		#       candidate.objects.bullk_create(list)
		#       return Response({"status":"Successfully inserted"},status=status.HTTP_201_CREATED)
		# except ValidationError as e:
		#   continue
		#   return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)
# try:
#   list=[]
#   user=(**user)
#   user.full_clean()
#   user.append(list)
#   candidate.objects.bullk_create(list)
# except:
#  validation.errors
#  continoue    

# #                         # dob=row[5],
# #                         # gender=row[6],
# #                         # sslc_marks=row[7],
# #                         # puc_marks=row[8],
# #                         # bachelor_degree=row[9],
# #                         # bachelor_degree_course=row[10],
# #                         # bachelor_degree_marks=row[11],
# #                         # master_degree=row[12],
# #                         # master_degree_course=row[13],
# #                         # master_degree_marks=row[14],
# #                         # address=row[15],
# #                         # tech_skills=row[16],
# #                         # prefered_location=row[17],
# #                         # previous_company=row[18],
# #                         # work_experience=row[19],
# #                         # current_ctc=row[20],
# #                         # expected_ctc=row[21],
# #                         # notice_period=row[22],
# #                         # resume= row[23],
# #                         # status=row[24]
					   
				

				# print(data)
			# print(i['first_name'])
			# print(to_db)
			# print(dr)

			# to_db = [(i['col1'], i['col2']) for i in dr]


			