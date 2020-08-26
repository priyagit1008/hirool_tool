# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import serializers
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
import os,io

import csv

from rest_framework.permissions import IsAuthenticated
from accounts.users.permissions import HiroolReadOnly,HiroolReadWrite
import json
from api.default_settings import MEDIA_ROOT,JSON_MEDIA_ROOT



# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
)
from libs.pagination import StandardResultsSetPagination

from libs.exceptions import ParseException

# app level imports
from .models import Client, Job 
from .services import ClientServices

from .services import JobServices


from .serializers import (
	ClientCreateRequestSerializer,
	ClientListSerializer,
	ClientUpdateSerializer,
	
	ClientDrowpdownGetSerializer,

	JobCreateRequestSerializer,
	JobListSerializer,
	JobGetSerializer,
	JobUpdateSerilaizer,
	JobDrowpdownGetSerializer,
)


# class CreateUserView(CreateAPIView):
#     model = get_user_model()
#     permission_classes = [
#         permissions.AllowAny # Or anon users can't register
#     ]
#     serializer_class = UserRegSerializer


class ClientViewSet(GenericViewSet):
	"""
	"""
	permissions=(HiroolReadOnly,HiroolReadWrite)
	queryset = Client.objects.all().order_by('-created_at')
	pagination_class = StandardResultsSetPagination

	# paginator = Paginator(queryset, 10)
	services = ClientServices()
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'client_add': ClientCreateRequestSerializer,
		'client_details': ClientCreateRequestSerializer,
		'client_list': ClientListSerializer,
		'client_dropdown_list':ClientDrowpdownGetSerializer,
		'client_update': ClientUpdateSerializer,
		'client_get':ClientListSerializer,
		'delete_client': ClientListSerializer,

	}

	def get_queryset(self,filterdata=None):
		if filterdata:
			self.queryset = Client.objects.filter(**filterdata)
		return self.queryset

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)




	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,],)
	def client_add(self, request):
		"""
		Returns clients account creations
		"""
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException({'status':'Incorrect input'}, serializer.errors)
		if Client.objects.filter(name=self.request.data['name']).exists():
			return Response({"status":"Client already exists"},status=status.HTTP_400_BAD_REQUEST)

		print("create client with", serializer.validated_data)

		client = serializer.create(serializer.validated_data)
		if client:
			return Response({'status':'Successfully added'}, status=status.HTTP_201_CREATED)

		return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ],)
	def client_details(self, request):
		"""
		Returns client details
		"""
		client_id = request.GET.get("id")
		try:
			client_obj = Client.objects.get(id=client_id)
			client_data = self.get_serializer(client_obj).data
			return Response(client_data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	def query_string(self,filterdata):
		dictionary={}
			 
		if "name" in filterdata:
			dictionary["name"] = filterdata.pop("name")
		if "category" in filterdata:
			dictionary["category__icontains"] = filterdata.pop("category")
		if "industry" in filterdata:
			dictionary["industry__icontains"] = filterdata.pop("industry")




		if "name" in filterdata:
			filterdata["name__icontains"] = filterdata.pop("name")
			return filterdata
		if "category" in filterdata:
			filterdata["category__icontains"] = filterdata.pop("category")
		if "industry" in filterdata:
			filterdata["industry__icontains"] = filterdata.pop("industry")
		return dictionary


	@action(
		methods=['get'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated,HiroolReadOnly, ],
	)
	def client_list(self, request,**dict):
		"""
		Return user list data and groups
		"""
		try:
			filterdata = self.query_string(request.query_params.dict())
			page = self.paginate_queryset(self.get_queryset(filterdata))
			serializer = self.get_serializer(page,many=True)

			return self.get_paginated_response(serializer.data)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(
		methods=['get'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def client_dropdown_list(self, request, **dict):
		"""
		Return user list data and groups
		"""
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get','put'], detail=False, permission_classes=[IsAuthenticated, ],)
	def client_update(self,request):
		"""
		Returns client update
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_client_service(id),data=request.data)
			if not serializer.is_valid():
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()    
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:

			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	

	@action(methods=['get', 'patch'],detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated,],
	)
	def client_get(self, request):
		"""
		Return client singal data and groups
		"""
		# print(request)
		id= request.GET.get('id', None)
		if not id:
				return Response({"status": False, "message":"id is required"})
		try:
			serializer=self.get_serializer(self.services.get_client_service(id))
		except Client.DoesNotExist:
			
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
		return Response(serializer.data, status.HTTP_200_OK)
			

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,])
	def delete_client(self,request):
		"""
		Returns delete interview
		"""
		id= request.GET.get('id', None)
		if not id:
				return Response({"status": False, "message":"id is required"})
		try:
			client_obj = self.services.get_client_service(id)
		except Client.DoesNotExist:
			raise
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
		client_obj.delete()
		return Response({"status":"clients is deleted "}, status.HTTP_200_OK)
			


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def client_column_jsondata(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('client_columns.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def category_response(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('category_response.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def industry_response(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('industry_response.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)




	@action(
		methods=['get'],
		detail=False,permission_classes=[],
	)
	def client_bulk_uplode(self,request):
		# fileForInput = open('sample.csv','r')
		# print(request.object)
		f=request.FILES['file']
		file = f.read().decode('utf-8').splitlines()

		try:
			dr=csv.DictReader(file)
			cand=Client()
			clients=[]
			for row in dr:
				client_obj=Client(**row)
				try:
					client_obj.full_clean()
				except ValidationError:
					continue
				clients.append(client_obj)

			d1=(len(clients))
			data=Client.objects.bulk_create(clients)
			return Response({"status":"Successfully inserted","total clients":d1},status=status.HTTP_201_CREATED)
		except Exception as e:
			
			return Response({"status":str(e)},status.HTTP_404_NOT_FOUND)






	# @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	# def clientindustry_list(self, request):

	#   data = self.get_serializer(self.services.get_queryset(),many=True).data
	#   return Response(data, status.HTTP_200_OK)





class JobViewSet(GenericViewSet):
	"""
	"""
	# queryset = Job.objects.all()
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)
	queryset=Job.objects.all().order_by('-created_at')
	pagination_class = StandardResultsSetPagination

	# paginator = Paginator(queryset, 10)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'job_add': JobCreateRequestSerializer,
		'job_get': JobGetSerializer,
		'job_list': JobListSerializer,
		'job_update':JobUpdateSerilaizer,
		'job_dropdown_list':JobDrowpdownGetSerializer,

	}

	# from .services import JobServices
	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = JobServices()

	# queryset = services.get_queryset()

	def get_queryset(self,filterdata=None):
		if filterdata:
			self.queryset = Job.objects.filter(**filterdata)
		return self.queryset
	 
	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)



	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def job_add(self, request):
		"""
		Returns jd details
		"""
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():

			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create job with", serializer.validated_data)

		job_obj = serializer.create(serializer.validated_data)
		if job_obj:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ],)
	def job_get(self, request):
		"""
		Returns single jd details
		"""
		id= request.GET.get('id', None)
		if not id:
				return Response({"status": False, "message":"id is required"})
		try:
			serializer=self.get_serializer(self.services.get_job_service(id))
		except Client.DoesNotExist:
			
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
		return Response(serializer.data, status.HTTP_200_OK)


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,],)
	def job_dropdown_list(self, request,**dict):
		"""
		Returns all jd details
		"""
		try:
			filter_data = request.query_params.dict()
			serializer=self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	def job_query_string(self,filterdata):
		dictionary={}
			 
		if "client" in filterdata:
			dictionary["client__name"] = filterdata.pop("client")
		if "job_title" in filterdata:
			dictionary["job_title"] = filterdata.pop("job_title")
		if "tech_skills" in filterdata:
			dictionary["tech_skills"] = filterdata.pop("tech_skills")
		if "job_location" in filterdata:
			dictionary["job_location"] = filterdata.pop("job_location")
		if "min_exp" in filterdata:
			dictionary["min_exp__gte"] = filterdata.pop("min_exp")
		if "max_exp" in filterdata:
			dictionary["max_exp__lte"] = filterdata.pop("max_exp")
		if "min_ctc" in filterdata:
			dictionary["min_ctc__gte"] = filterdata.pop("min_ctc")
		if "max_ctc" in filterdata:
			dictionary["max_ctc__lte"] = filterdata.pop("max_ctc")
		if "qualification" in filterdata:
			dictionary["qualification"] = filterdata.pop("qualification")
		if "percentage_criteria" in filterdata:
			dictionary["percentage_criteria"] = filterdata.pop("percentage_criteria")
		if "min_notice_period" in filterdata:
			dictionary["min_notice_period__gte"] = filterdata.pop("min_notice_period")
		if "max_notice_period" in filterdata:
			dictionary["max_notice_period__lte"] = filterdata.pop("max_notice_period")


		if "client" in filterdata:
			filterdata["client__name"] = filterdata.pop("client")

		if "job_title" in filterdata:
			filterdata["job_title__icontains"] = filterdata.pop("job_title")

		if "tech_skills" in filterdata:
			filterdata["tech_skills__icontains"] = filterdata.pop("tech_skills")

		if "job_location" in filterdata:
			filterdata["job_location__icontains"] = filterdata.pop("job_location")

		if "min_exp" in filterdata:
			filterdata["min_exp__gte"] = filterdata.pop("min_exp")

		if "max_exp" in filterdata:
			filterdata["max_exp__lte"] = filterdata.pop("max_exp")

		if "min_ctc" in filterdata:
			filterdata["min_ctc__gte"] = filterdata.pop("min_ctc")

		if "max_ctc" in filterdata:
			filterdata["max_ctc__lte"] = filterdata.pop("max_ctc")

		if "qualification" in filterdata:
			filterdata["qualification__icontains"] = filterdata.pop("qualification")

		if "percentage_criteria" in filterdata:
			filterdata["percentage_criteria__icontains"] = filterdata.pop("percentage_criteria")

		if "min_notice_period" in filterdata:
			filterdata["min_notice_period__gte"] = filterdata.pop("min_notice_period")

		if "max_notice_period" in filterdata:
			filterdata["max_notice_period__lte"] = filterdata.pop("max_notice_period")
		return dictionary



	
	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,],)
	def job_list(self, request,**dict):
		"""
		Returns all jd details
		"""
		try:
			filterdata = self.job_query_string(request.query_params.dict())
			page = self.paginate_queryset(self.get_queryset(filterdata))
			serializer = self.get_serializer(page,many=True)

			return self.get_paginated_response(serializer.data)

			# return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['get','put'], detail=False, permission_classes=[IsAuthenticated,],)
	def job_update(self,request):
		"""
		Returns jd edit
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_job_service(id),data=request.data)
			if not serializer.is_valid():

				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:
			
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	@action(
		methods=['get'],
		detail=False,permission_classes=[],
	)
	def job_bulk_uplode(self,request):
		# fileForInput = open('sample.csv','r')
		# print(request.object)
		f=request.FILES['file']		
		decode= f.read().decode('utf-8').splitlines()

		try:
			dr=csv.DictReader(decode)
			cand=Job()
			jobs=[]
			for row in dr:
				job_obj=Job(**row)
				try:
					job_obj.full_clean()
				except ValidationError:
					continue
				jobs.append(job_obj)

			d1=(len(jobs))
			data=Job.objects.bulk_create(jobs)
			return Response({"status":"Successfully inserted","total jobs":d1},status=status.HTTP_201_CREATED)
		except Exception as e:
			
			return Response({"status":str(e)},status.HTTP_404_NOT_FOUND)



	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def job_column_jsondata(self, request):
		file_path = os.path.join(JSON_MEDIA_ROOT,str('job_columns.json'))
		myfile= open(file_path,'r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		return Response(obj)

