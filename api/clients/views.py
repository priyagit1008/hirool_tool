# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import serializers

# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from accounts.users.permissions import HiroolReadOnly,HiroolReadWrite
import json 


# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
)
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
	# ClientGetSerializer,
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
	services = ClientServices()
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'org': ClientCreateRequestSerializer,
		'org_details': ClientCreateRequestSerializer,
		'org_list': ClientListSerializer,
		'org_dropdown_list':ClientDrowpdownGetSerializer,
		'org_update': ClientUpdateSerializer,
		'org_get':ClientListSerializer,
		'delete_client': ClientListSerializer,

		# 'org_dropdown':ClientGetSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)




	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,],)
	def org(self, request):
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
	def org_details(self, request):
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

	@action(
		methods=['get'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def org_list(self, request, **dict):
		"""
		Return user list data and groups
		"""
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(
		methods=['get'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def org_dropdown_list(self, request, **dict):
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
	def org_update(self,request):
		"""
		Returns client update
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_client_service(id),data=request.data)
			if not serializer.is_valid():
				print(serializer.errors)
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()    
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	

	@action(methods=['get', 'patch'],detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated,],
	)
	def org_get(self, request):
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
			raise
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
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/client_columns.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		return Response(obj)


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def category_response(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/category_response.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		print("hi")
		return Response(obj)

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def industry_response(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/industry_response.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		print("hi")
		return Response(obj)





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

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'job': JobCreateRequestSerializer,
		'job_get': JobGetSerializer,
		'job_list': JobListSerializer,
		'job_update':JobUpdateSerilaizer,
		'job_dropdown_list':JobDrowpdownGetSerializer,

	}

	# from .services import JobServices
	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = JobServices()

	# queryset = services.get_queryset()

  
	 
	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)



	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def job(self, request):
		"""
		Returns jd details
		"""
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			print(serializer.errors)
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
			raise
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


	
	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,],)
	def job_list(self, request,**dict):
		"""
		Returns all jd details
		"""
		try:
			filter_data = request.query_params.dict()
			serializer=self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


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
				print(serializer.errors)
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def job_column_jsondata(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/job_columns.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		return Response(obj)

