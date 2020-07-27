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
from django.core.paginator import Paginator

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
	queryset = LeaveTracker.objects.all()
	paginator = Paginator(queryset, 10)

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


	def get_queryset(self,filterdata=None):
		if filterdata:
			self.queryset = LeaveTracker.objects.filter(**filterdata)
		return self.queryset



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



	def leave_query_string(self,filterdata):


		if "leave_type" in filterdata:
			filterdata["leave_type__leave_type"] = filterdata.pop("leave_type")

		if "leave_status" in filterdata:
			filterdata["leave_status__icontains"] = filterdata.pop("leave_status")

		if "from_date" in filterdata:
			filterdata["from_date__gte"] = filterdata.pop("from_date")

		if "to_date" in filterdata:
			filterdata["to_date__lte"] = filterdata.pop("to_date")
			
		if "approved_by" in filterdata:
			filterdata["approved_by__icontains"] = filterdata.pop("approved_by")
		return filterdata


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,], )
	def leave_list(self, request, **dict):
		try:
			filterdata = self.leave_query_string(request.query_params.dict())
			page = self.paginator.get_page(self.get_queryset(filterdata))
			serializer = self.get_serializer(page, many=True)
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
			raise ParseException({'status':'Incorrect Input'}, serializer.errors)
		leavetype_obj = serializer.create(serializer.validated_data)

		if leavetype_obj:
			msg_plain = render_to_string('interview_email_message.txt', {"name":interview.candidate.first_name,"date": interview.date,"location":interview.location})
			msg_html = render_to_string('interview_email.html',{"name":interview.candidate.first_name,"date": interview.date,"location":interview.location})
			send_mail('Hirool', msg_plain, settings.EMAIL_HOST_USER, [interview.candidate.email],html_message=msg_html, )
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




