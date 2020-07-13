from django.shortcuts import render
from libs.helpers import time_it

# Create your views here.
from django.conf import settings
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from accounts.users.permissions import HiroolReadOnly, HiroolReadWrit

# project level imports
from libs.constants import (
	BAD_REQUEST,
	BAD_ACTION,
)

from libs.exceptions import ParseException
# app level imports
from .models import  LeaveType,LeaveTracker

# project level imports
from accounts.models import User

from .serializers import (
	LeavetrackerRequestSerializer,
	LeavetrackerListSerializer,
	LeaveUpdateSerilaizer,
	LeavestatusDrowpdownGetSerializer,
	LeaveTypeRequestSerializer,
	LeaveTypeDrowpdownGetSerializer,
	LeaveTypeListSerializer,
	# LeaveStatusRequestSerializer,
	# LeaveStatusListSerializer

	)

from .services import LeaveTrackerServices
from .services import LeaveType_Services

# from .services import LeaveStatus_Services






class LeaveTrackerViewSet(GenericViewSet):
	"""docstring for interview"""

	services = LeaveTrackerServices()

	# queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_leave': LeavetrackerRequestSerializer,
		'get_leave': LeavetrackerListSerializer,
		'leavestatus_dropdown':LeavestatusDrowpdownGetSerializer,
		'leave_update':LeaveUpdateSerilaizer,
		'leave_list':LeavetrackerListSerializer,

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
	def add_leave(self, request):

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException({'status':'Incorrect input'}, serializer.errors)

		print("create client with", serializer.validated_data)

		leavetracker_obj = serializer.create(serializer.validated_data)
		if leavetracker_obj:
			return Response({'status':'Successfully added'}, status=status.HTTP_201_CREATED)

		return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)





	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
	def get_leave(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id= request.GET.get('id', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.get_leave_service(id))
				return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,], )
	def leavestatus_dropdown(self, request, **dict):
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.leave_filter_service(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['put'], detail=False, permission_classes=[IsAuthenticated,], )
	def leave_update(self, request):
		"""
		Return user profile data and groups
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_leave_service(id),data=request.data)
			if not serializer.is_valid():
				print(serializer.errors)
				raise ParseException({'status':'Incorrect Input'},serializer.errors)
			else:
				serializer.save()    
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)




	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,], )
	def leave_list(self, request, **dict):
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.leave_filter_service(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)





class LeaveTypeViewSet(GenericViewSet):
	"""docstring for interview"""

	services = LeaveType_Services()

	# queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_leavetype': LeaveTypeRequestSerializer,
		'get_leavetype': LeaveTypeListSerializer,
		'leavetype_dropdown':LeaveTypeDrowpdownGetSerializer,
		'leavetype_list':LeaveTypeListSerializer,

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

	def add_leavetype(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException({'status':'Incorrect Input'}, serializer.errors)
		leavetype_obj = serializer.create(serializer.validated_data)

		if leavetype_obj:
			# msg_plain = render_to_string('interview_email_message.txt', {"name":interview.candidate.first_name,"date": interview.date,"location":interview.location})
			# msg_html = render_to_string('interview_email.html',{"name":interview.candidate.first_name,"date": interview.date,"location":interview.location})
			# send_mail('Hirool', msg_plain, settings.EMAIL_HOST_USER, [interview.candidate.email],html_message=msg_html, )
			return Response(serializer.data,status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
	def get_leavetype(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id= request.GET.get('id', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.get_leavetype_service(id))
				return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,], )
	def leavetype_dropdown(self, request, **dict):
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.LeaveType_filter_service(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,], )
	def leavetype_list(self, request, **dict):
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.LeaveType_filter_service(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



# class LeaveStatusViewSet(GenericViewSet):
# 	"""docstring for interview"""

# 	services = LeaveStatus_Services()

# 	# queryset = services.get_queryset()

# 	filter_backends = (filters.OrderingFilter,)
# 	authentication_classes = (TokenAuthentication,)

# 	ordering_fields = ('id',)
# 	ordering = ('id',)
# 	lookup_field = 'id'
# 	http_method_names = ['get', 'post', 'put']

# 	serializers_dict = {
# 		'add_leavestatus': LeaveStatusRequestSerializer,
# 		'get_leavesatus': LeaveStatusListSerializer,
# 		'leavesatus_list':LeaveStatusListSerializer,

# 	}

# 	def get_serializer_class(self):
# 		"""
# 		:return:
# 		"""
# 		try:
# 			return self.serializers_dict[self.action]
# 		except KeyError as key:
# 			raise ParseException(BAD_ACTION, errors=key)

# 	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
# 	def add_leavestatus(self, request):

# 		serializer = self.get_serializer(data=request.data)
# 		if serializer.is_valid() is False:
# 			print(serializer.errors)
# 			raise ParseException(BAD_REQUEST, serializer.errors)
			
# 		leavestatus = serializer.create(serializer.validated_data)
# 		if leavestatus:
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)

# 		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



# 	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
# 	def get_leavesatus(self, request):
# 		"""
# 		Return client profile data and groups
# 		"""
# 		try:
# 			id= request.GET.get('id', None)
# 			if not id:
# 				return Response({"status": "Failed", "message":"id is required"})
# 			else:
# 				serializer = self.get_serializer(self.services.get_leavestatus_service(id))
# 				return Response(serializer.data, status.HTTP_200_OK)
# 		except Exception as e:
# 			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


# 	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,], )
# 	def leavesatus_list(self, request, **dict):
# 		try:
# 			filter_data = request.query_params.dict()
# 			serializer = self.get_serializer(self.services.LeaveStatus_filter_service(filter_data), many=True)
# 			return Response(serializer.data, status.HTTP_200_OK)
# 		except Exception as e:
# 			raise
# 			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
from django.shortcuts import render

# Create your views here.
