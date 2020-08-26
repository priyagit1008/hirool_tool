# Create your views here.
# django imports
from django.conf import settings
import os,io

from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.users.permissions import HiroolReadOnly, HiroolReadWrite
from django.template.loader import render_to_string
from django.core.mail import send_mail
import json 
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

import csv
from api.default_settings import MEDIA_ROOT,JSON_MEDIA_ROOT




# project level imports
from libs.constants import (
	BAD_REQUEST,
	BAD_ACTION,
)
from libs.exceptions import ParseException
from libs.pagination import StandardResultsSetPagination


# app level imports
from .models import Interview, InterviewRound, InterviewStatus
# project level imports
from clients.models import Client, Job
from accounts.models import User
from candidate.models import Candidate
# from .services import ClientServices

from .serializers import (
	InterviewCreateRequestSerializer,
	# InterviewGetSerializer,
	InterviewListSerializer,
	InterviewUpdateSerilaizer,
	InterviewRoundRequestSerializer,
	InterviewRoundDrowpdownGetSerializer,
	InterviewRoundListSerializer,
	InterviewStatusRequestSerializer,
	InterviewStatusDrowpdownGetSerializer,
	InterviewStatusListSerializer
)

from .services import InterviewServices
from .services import InterviewRound_Services
from .services import InterviewStatus_Services


class InterviewViewSet(GenericViewSet):
	"""docstring for ClassName"""
	permissions = (HiroolReadOnly, HiroolReadWrite)
	services = InterviewServices()
	queryset=Interview.objects.all().order_by('-created_at')
	pagination_class = StandardResultsSetPagination

	# paginator = Paginator(queryset, 10)



	# queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)
	

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'interview_add': InterviewCreateRequestSerializer,
		'interview_get': InterviewListSerializer,
		'interview_list': InterviewListSerializer,
		'interview_update': InterviewUpdateSerilaizer,
		'delete_interview': InterviewListSerializer,
	}

	def get_queryset(self,filterdata=None):
		if filterdata:
			self.queryset = Interview.objects.filter(**filterdata)

		return self.queryset

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,], )

	def interview_add(self, request):

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:

			raise ParseException({'status':'Incorrect Input'}, serializer.errors)
		interview = serializer.create(serializer.validated_data)

		if interview:
			msg_plain = render_to_string('interview_email_message.txt', {"name":interview.candidate.first_name,"date": interview.date,"location":interview.location})
			msg_html = render_to_string('interview_email.html',{"name":interview.candidate.first_name,"date": interview.date,"location":interview.location})
			send_mail('Hirool', msg_plain, settings.EMAIL_HOST_USER, [interview.candidate.email],html_message=msg_html, )
			return Response({'status':'Successfully added'},status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated,], )
	def interview_get(self, request):
		id= request.GET.get('id', None)
		if not id:
				return Response({"status": False, "message":"id is required"})
		try:
			serializer = self.get_serializer(self.services.get_interview_service(id))
		except Interview.DoesNotExist:
			
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
		return Response(serializer.data, status.HTTP_200_OK)



	def interview_query_string(self,filterdata):
		dictionary={}
			 
		if "client" in filterdata:
			dictionary["client__name"] = filterdata.pop("client")
		if "job" in filterdata:
			dictionary["job__job_title"] = filterdata.pop("job")
		if "candidate" in filterdata:
			dictionary["candidate__email"] = filterdata.pop("candidate")
		if "interview_round" in filterdata:
			dictionary["interview_round__interview_round"] = filterdata.pop("interview_round")
		if "interview_status" in filterdata:
			dictionary["interview_status__status"] = filterdata.pop("interview_status")
		if "location" in filterdata:
			dictionary["location__icontains"] = filterdata.pop("location")
		if "date_from" in filterdata:
			dictionary["date__gte"] = filterdata.pop("date_from")
		if "date_to" in filterdata:
			dictionary["date__lte"] = filterdata.pop("date_to")
		# if "job" in filterdata:
		# 	dictionary["job__job_title"] = filterdata.pop("job")
		# if "job" in filterdata:
		# 	dictionary["job__job_title"] = filterdata.pop("job")


		if "client" in filterdata:
			filterdata["client__name"] = filterdata.pop("client")

		if "job" in filterdata:
			filterdata["job__job_title"] = filterdata.pop("job")

		if "candidate" in filterdata:
			filterdata["candidate__email"] = filterdata.pop("candidate")

		if "interview_round" in filterdata:
			filterdata["interview_round__interview_round"] = filterdata.pop("interview_round")

		if "interview_status" in filterdata:
			filterdata["interview_status__status"] = filterdata.pop("interview_status")

		if "location" in filterdata:
			filterdata["location__icontains"] = filterdata.pop("location")

		if "date_from" in filterdata:
			filterdata["date__gte"] = filterdata.pop("date_from")

		if "date_to" in filterdata:
			filterdata["date__lte"] = filterdata.pop("date_to")
		return dictionary



	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,],)
	def interview_list(self, request,**dict):
		"""
		Returns all jd details
		"""
		try:
			filterdata = self.interview_query_string(request.query_params.dict())
			page = self.paginate_queryset(self.get_queryset(filterdata))
			serializer = self.get_serializer(page,many=True)

			return self.get_paginated_response(serializer.data)
		except Exception as e:
			
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['put'], detail=False, permission_classes=[IsAuthenticated,HiroolReadOnly], )
	def interview_update(self, request):
		"""
		Return user profile data and groups
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_interview_service(id),data=request.data)
			if not serializer.is_valid():
				print(serializer.errors)
				raise ParseException({'status':'Incorrect Input'},serializer.errors)
			else:
				serializer.save()    
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:
			
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)




	@action(methods=['get'], detail=False, permission_classes=[])
	def delete_interview(self,request):
		"""
		Returns delete interview
		"""
		id= request.GET.get('id', None)
		if not id:
				return Response({"status": False, "message":"id is required"})
		try:
			interview_obj = self.services.get_interview_service(id)
		except Interview.DoesNotExist:
			
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
		interview_obj.delete()
		return Response({"status":"interview is deleted "}, status.HTTP_200_OK)



	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def interview_columns(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('interview_columns.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def interview_status(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('interview_status.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def interview_round(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('interview_round.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)



	@action(
		methods=['get'],
		detail=False,permission_classes=[],
	)
	def interview_bulk_uplode(self,request):
		# fileForInput = open('sample.csv','r')
		# print(request.object)
		f=request.FILES['file']		
		decode= f.read().decode('utf-8').splitlines()

		try:
			dr=csv.DictReader(decode)
			cand=Job()
			interviews=[]
			for row in dr:

				interview_obj=Interview(**row)
				try:
					interview_obj.full_clean()
				except ValidationError:
					continue
				interviews.append(interview_obj)

			d1=(len(interviews))
			data=Interview.objects.bulk_create(interviews)
			return Response({"status":"Successfully inserted","total jobs":d1},status=status.HTTP_201_CREATED)
		except Exception as e:
			
			return Response({"status":str(e)},status.HTTP_404_NOT_FOUND)






###################################################################################


class InterviewRoundViewSet(GenericViewSet):
	"""docstring for interview"""

	services = InterviewRound_Services()

	# queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_round': InterviewRoundRequestSerializer,
		'round_get': InterviewRoundListSerializer,
		# 'round_list': InterviewRoundListSerializer,
		'inetrviewround_dropdown':InterviewRoundDrowpdownGetSerializer,

	}

	def get_serializer_class(self):
		"""
		:return:
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_round(self, request):

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		interview = serializer.create(serializer.validated_data)
		if interview:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
	def round_get(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id= request.GET.get('id', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.get_Round_service(id))
				return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,], )
	def inetrviewround_dropdown(self, request, **dict):
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.interviewround_filter_service(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


class InterviewStatusViewSet(GenericViewSet):
	services = InterviewStatus_Services()

	# queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_status': InterviewStatusRequestSerializer,
		'status_get': InterviewStatusListSerializer,
		'inetrviewstatus_dropdown':InterviewStatusDrowpdownGetSerializer,
		# 'status_list': InterviewStatusListSerializer,
	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_status(self, request):

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)
		interview = serializer.create(serializer.validated_data)
		if interview:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
	def status_get(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id= request.GET.get('id', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.get_status_service(id))
				return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
				return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,], )
	def inetrviewstatus_dropdown(self, request, **dict):
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.interviewstatus_filter_service(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	# @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	# def status_list(self, request):

	# 	data = self.get_serializer(self.queryset, many=True).data
	# 	return Response(data, status.HTTP_200_OK)
