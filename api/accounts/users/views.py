# django imports
from rest_framework import filters
import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.db.models.functions import Trunc
from django.db.models.functions import TruncMonth,TruncDay,TruncDate
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth,ExtractYear
from django.contrib.auth import authenticate

from datetime import datetime

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import HiroolReadOnly

from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.conf import settings
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination

# app level imports
from .models import User, Actions, Permissions, UserPermissions,UserRole
from clients.models import Client,Job
from candidate.models import Candidate
from interview.models import  Interview

# from templates 

from .serializers import (
	UserLoginRequestSerializer,
	UserRegSerializer,
	UserListSerialize,
	UserGetSerializer,
	UserUpdateRequestSerializer,
	UserPassUpdateSerializer,
	UserDrowpdownGetSerializer,

	UserRoleCreateRequestSerializer,
	UserRoleListSerializer,

	UserPermissionCreateRequestSerializer,
	UserPermissionsListSerializer,

	PermissionCreateRequestSerializer,
	PermissionsListSerializer,

	ActionCreateRequestSerializer,
	ActionListSerializer
)

from .services import UserServices
from .services import userpermissions_service
from .services import permission_service
from .services import action_service,UserRoleService

# project level imports
from libs.constants import (
	BAD_REQUEST,
	BAD_ACTION,
	# ParseException

)
from libs import (
	# redis_client,
	otpgenerate,
	mail,
)
from libs.clients import (
	redis_client
)
from libs.exceptions import ParseException
from libs.pagination import CursorSetPagination



class UserViewSet(GenericViewSet):
	"""
	"""
	permissions = (HiroolReadOnly,)
	pagination_class = CursorSetPagination
	queryset=User.objects.all()
	# pagination_class = PageNumberPagination
	# paginator = Paginator(queryset, 10)
	# page_size = 1



	services = UserServices()
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'login': UserLoginRequestSerializer,
		'register': UserRegSerializer,
		'list_exec': UserListSerialize,
		'exec_get': UserListSerialize,
		'exec_update': UserUpdateRequestSerializer,
		'forgotpass': UserPassUpdateSerializer,
		'update_pass': UserPassUpdateSerializer,
		'user_profile':UserListSerialize, 
		'user_dropdown':UserDrowpdownGetSerializer ,
		'delete_user':UserListSerialize }


	def get_queryset(self,filterdata=None):
		if filterdata:
			self.queryset =User.objects.filter(**filterdata)
		return self.queryset

	def get_serializer_class(self):
		"""
		Returns serilizer class
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[])
	def register(self, request):
		"""
		Returns user account creationsm
		"""
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException({'status':'Incorrect Input'}, serializer.errors)
		if User.objects.filter(email=self.request.data['email']).exists():
			return Response({"status":"User already exists"},status=status.HTTP_400_BAD_REQUEST)
		user = serializer.create(serializer.validated_data)
		if user:
				# msg_plain = render_to_string('email_message.txt', {"user": user.first_name})
				# msg_html = render_to_string('email.html', {"user": user.first_name})
				# send_mail('Hirool', msg_plain, settings.EMAIL_HOST_USER, [user.email], html_message=msg_html)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
		



	@action(methods=['post'], detail=False, permission_classes=[])
	def login(self, request):
		"""
		Return user login
		"""
		serializer = self.get_serializer(data=request.data)


		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		user = authenticate(
			email=serializer.validated_data["email"],
			password=serializer.validated_data["password"])
		if not user:
			return Response({'status': 'Invalid Credentials'},
							status=status.HTTP_404_NOT_FOUND)
		token = user.access_token
		name= user.first_name
		id=user.id
		return Response({'token': token,"name":name,'user_id':id},
						status=status.HTTP_200_OK)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
	def logout(self, request):
		"""
		Return user logout
		"""
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)


	def user_query_string(self,filterdata):
		if "work_location" in filterdata:
			filterdata["work_location__icontains"] = filterdata.pop("work_location")

		if "designation" in filterdata:
			filterdata["designation__icontains"] = filterdata.pop("designation")

		if "status" in filterdata:
			filterdata["status__icontains"] = filterdata.pop("status")

		if "reporting_to" in filterdata:
			filterdata["reporting_to__gte"] = filterdata.pop("reporting_to")

		if "joined_date_from" in filterdata:
			filterdata["joined_date__gte"] = filterdata.pop("joined_date_from")

		if "joined_date_to" in filterdata:
			filterdata["joined_date__lte"] = filterdata.pop("joined_date_to")

		if "resigned_date_from" in filterdata:
			filterdata["resigned_date__gte"] = filterdata.pop("resigned_date_from")

		if "resigned_date_to" in filterdata:
			filterdata["resigned_date__lte"] = filterdata.pop("resigned_date_to")
			
		return filterdata

	# def  user_query_set(self,filterdata):
	# 	if "name" in filterdata:
	# 		filtename = filterdata.copy("filterdata")


		
	@action(
		methods=['get'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)


	def list_exec(self, request,**dict):
		"""
		Return user list data and groups
		"""

		try:
			filterdata = self.user_query_string(request.query_params.dict())
			result_page = paginator.paginate_queryset(PostServices.post_feed(filterdata=filterdata))

			page = self.paginate_queryset(self.get_queryset(filterdata))
			serializer = self.get_serializer(page,many=True)
			return self.get_paginated_response(serializer.data)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


    
	@action(
		methods=['get'],
		detail=False,
		# url_path='image-upload',
		# permission_classes=[IsAuthenticated, ],
	)
	def user_dropdown(self, request, **dict):
		"""
		Return user list data and groups
		"""
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.get_user_dropdown_queryset(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
	

	def dashboard(self, request, **dict):
		"""
		Return user list data and groups
		"""
		try:
			# filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)





	@action(methods=['get', 'patch'],
			detail=False,
			# url_path='image-upload',
			permission_classes=[IsAuthenticated, ], )
	def user_profile(self, request):
		"""
		Return user profile data and groups
		"""
		try:
			id=request.GET["id"]
			serializer=self.get_serializer(self.services.get_user(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(
		methods=['get', 'put'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def exec_update(self, request):
		"""
		Return user update data
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_user(id),data=request.data)
			if not serializer.is_valid():
				print(serializer.errors)
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()    
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	


	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated],)
	def exec_get(self,request):
		"""
		Returns single candidate details
		"""
		id= request.GET.get('id', None)
		if not id:
				return Response({"status": False, "message":"id is required"})
		try:
			serializer = self.get_serializer(self.services.get_user(id))
		except User.DoesNotExist:
			raise
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
		return Response(serializer.data, status.HTTP_200_OK)



		# try:
		# 	id= request.GET.get('id', None)
		# 	if not id:
		# 		return Response({"status": "Failed", "message":"id is required"})

		# 	serializer = self.get_serializer(self.services.get_user(id))
		# 	# data = {
		# 	#   "user": serializer.data,
		# 	#   "user1": UserListSerializer(self.services.get_user(id)).data
		# 	# }
		# 	return Response(serializer.data,status.HTTP_200_OK)
		# except Exception as e:
		# 	raise
		# 	return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	# @action(
	# 	methods=['put'],
	# 	detail=False,
	# 	# url_path='image-upload',
	# 	permission_classes=[IsAuthenticated, ],
	# )

	@action(
		methods=['get'],
		detail=False, permission_classes=[IsAuthenticated, ],
	)
	def send_otp(self, request):
		"""
		send otp api
		"""
		try:
			email = request.GET.get('email', None)
			if not email:
				return Response({"status": "Failed", "message":"email  is required"})
			else:
				user_obj = self.services.email_service(email)  
				otp = otpgenerate.otpgen(self)
				msg_plain = render_to_string('email_message.txt', {"user":request.user.email,"name":request.user.first_name})
				msg_html = render_to_string('otp_template.html', {"user":otp})
				redis_client.store_data(email, otp)
				send_mail('Hirool', msg_plain, settings.EMAIL_HOST_USER, [request.user.email], html_message=msg_html, )
				return Response({"status": "email sent"}, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['get'],
		detail=False, permission_classes=[IsAuthenticated, ], )
	def send_email(self, request):
		"""
		send mail api
		"""
		try:
			email = request.GET.get('email', None)
			if not email:
				return Response({"status": "Failed", "message":"email  is required"})
			else:
				user_obj = User.objects.get(email=email,is_active=True)
				otp = otpgenerate.otpgen(self)
				print(otp)
				redis_client.store_data(email,otp)
				print(redis_client.get_Key_data(email))
				mail.sendmail.delay(otp,"Forgate password",[request.user.email])
				return Response({"status":"email sent"}, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)


	@action(
		methods=['put'],
		detail=False, permission_classes=[IsAuthenticated, ],
	)
	def forgotpass(self, request):
		"""
		Returns forgot password
		"""
		try:
			data = request.data
			user_obj = User.objects.get(email=data["email"], is_active=True)
			if not redis_client.key_exists(data["email"]):
				print(data["email"])
				return Response({"status": "Bad Otp"}, status=status.HTTP_400_BAD_REQUEST)
			if not redis_client.get_Key_data(data["email"]):
				print(data["email"])
				return Response({"status": "Bad Otp"}, status=status.HTTP_400_BAD_REQUEST)

			redis_client.delete_Key_data(data["email"])

			serializer = self.get_serializer(user_obj, data=data)
			if not serializer.is_valid():
				return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
			try:
				serializer.save()
				return Response({"status": "Successfully Updated password"}, status.HTTP_200_OK)
			except Exception as e:
				return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)
		except Exception as e:
			raise
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['put'],
		detail=False,
		permission_classes=[IsAuthenticated, ],
	)
	def update_pass(self, request):
		"""
		update new password with validatig old password
		"""
		data = request.data
		user_obj = User.objects.get(id=request.user.id)
		serializer = self.get_serializer(user_obj, data=data)
		if not serializer.is_valid():
			raise ParseException(BAD_REQUEST, serializer.errors)
		try:
			if not user_obj.check_password(data.get("old_password")):
				return Response({"old_password is Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
			serializer.save()
			return Response({"status": "Successfully Updated new password"}, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,])
	def delete_user(self,request):
		"""
		Returns delete interview
		"""
		id= request.GET.get('id', None)
		if not id:
				return Response({"status": False, "message":"id is required"})
		try:
			user_obj = self.services.get_user(id)
		except User.DoesNotExist:
			raise
			return Response({"status": False}, status.HTTP_404_NOT_FOUND)
		user_obj.delete()
		return Response({"status":"user is deleted "}, status.HTTP_200_OK)
	

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def menu_sidebar(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/menu_sidebar.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		return Response(obj)


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def user_designation(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_filesuser_designation.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		return Response(obj)

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def user_columns(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_filesuser_columns.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		return Response(obj)
	

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def skills_dropdown(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/skills_dropdown.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		print("hi")
		return Response(obj)



	
	@action(
		methods=['get'],
		detail=False, permission_classes=[IsAuthenticated, ],
	)
	def user_dashboard(self, request):
		"""
		Return total users data
		"""
		user={
			"user_count":User.objects.count(),
			"active_user":User.objects.filter(is_active=True).count(),
			"closed_user":User.objects.filter(is_active=False).count()
			}

		interview={
			"interview_count ":Interview.objects.count(),
			"active_interview":Interview.objects.filter(is_active=True).count(),
			"closed_interview":Interview.objects.filter(is_active=False).count()
			}
		client={
			"client_count":Client.objects.count(),
			"active_Client":Client.objects.filter(is_active=True).count(),
			"closed_Client":Client.objects.filter(is_active=False).count()
			}
		job={
			"job_count":Job.objects.count(),
			"active_job":Job.objects.filter(is_active=True).count(),
			"closed_job":Job.objects.filter(is_active=False).count()}

		candidate={
			"candidate_count":Candidate.objects.count(),
			"active_candidate":Candidate.objects.filter(is_active=True).count(),
			"closed_candidate":Candidate.objects.filter(is_active=False).count()}

		interview={
			"interview_count":Interview.objects.count(),
			"active_interview":Interview.objects.filter(is_active=True).count(),
			"closed_interview":Interview.objects.filter(is_active=False).count()}



		return Response({"user": user,"interview":interview,"client":client,"jobs":job,"candidates":candidate,"interview":interview},status.HTTP_200_OK)

	
	@action(
		methods=['get'],
		detail=False, permission_classes=[],
	)
	def dashboard_graph(self, request):
		"""
		Return total users data
		"""
		# print(today.strftime('%B'))
		user={ "user":User.objects.annotate(month=TruncMonth('created_at')).
		values('month').annotate(total=Count('id')).order_by('created_at')}

		client={ "clients":Client.objects.annotate(month=TruncMonth('created_at')).
		values('month').annotate(total=Count('id')).order_by('created_at')}

		candidate={ "candidates":Candidate.objects.annotate(month=TruncMonth('created_at')).
		values('month').annotate(total=Count('id')).order_by()}

		jd={ "jd":Job.objects.annotate(month=TruncMonth('created_at')).
		values('month').annotate(total=Count('id')).order_by()}

		return Response({"user": user,"clients": client,"candidates": candidate,"jds": jd},status.HTTP_200_OK)



class UserRoleViewSet(GenericViewSet):
	"""
	"""
	services = UserRoleService()

	queryset = services.get_userall()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_userrole': UserRoleCreateRequestSerializer,
		'list_userrole': UserRoleListSerializer,
		# 'get_userrole': UserPermissionsListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[], )
	def add_userrole(self, request):
		"""
		Returns add userrole
		"""
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)
		userrole = serializer.create(serializer.validated_data)
		if userrole:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)

	@action(methods=['get'], detail=False, permission_classes=[], )
	def list_userrole(self, request):
		"""
		Return all role data
		"""
		data = self.get_serializer(self.get_userall(), many=True).data
		return Response(data, status.HTTP_200_OK)

	# @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	# def get_userrole(self, request):
	#   """
	#   Returns userpermission data
	#   """
	#   try:
	#       id = request.GET["id"]
	#       serializer = self.get_serializer(self.services.get_userpermission_service(id))
	#       return Response(serializer.data, status.HTTP_200_OK)
	#   except Exception as e:
	#       return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)






###################################################################################
class UserPermissionsViewSet(GenericViewSet):
	"""
	"""

	services = userpermissions_service()

	queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_userpermissions': UserPermissionCreateRequestSerializer,
		'list_userpermission': UserPermissionsListSerializer,
		'get_userpermission': UserPermissionsListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_userpermissions(self, request):
		"""
		Returns add userpermissions 
		"""
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)
		permissions = serializer.create(serializer.validated_data)
		if permissions:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	def list_userpermission(self, request):
		"""
		Return all permission data
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	def get_userpermission(self, request):
		"""
		Returns userpermission data
		"""
		try:
			id = request.GET["id"]
			serializer = self.get_serializer(self.services.get_userpermission_service(id))
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


###############################################################################

class PermissionsViewSet(GenericViewSet):
	"""
	"""

	services = permission_service()

	queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_permissions': PermissionCreateRequestSerializer,
		'list_permission': PermissionsListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_permissions(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create permissions with", serializer.validated_data)

		permissions = serializer.create(serializer.validated_data)
		if permissions:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	def list_permission(self, request):
		"""
		Return user profile data and groups
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)


############################################################################

class ActionViewSet(GenericViewSet):
	"""
	"""

	services = action_service()

	queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_actions': ActionCreateRequestSerializer,
		'list_actions': ActionListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_actions(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		action = serializer.create(serializer.validated_data)
		if action:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	def list_permission(self, request):
		"""
		Return user profile data and groups
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)
	


