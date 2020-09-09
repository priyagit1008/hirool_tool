# django imports
from rest_framework import filters
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
import json
import os,io
import base64

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.paginator import Paginator
from api.default_settings import MEDIA_ROOT,JSON_MEDIA_ROOT



# app level imports
from .permissions import HiroolReadOnly
from .models import User, Actions, Permissions, UserPermissions,UserRole
from clients.models import Client
from candidate.models import Candidate
from interview.models import  Interview
from leave_management.models import LeaveTracker


# from templates 

from .serializers import (
	UserLoginRequestSerializer,
	UserRegSerializer,
	UserListSerializer,
	UserGetSerializer,
	UserUpdateRequestSerializer,
	UserPassUpdateSerializer,
	UserDrowpdownGetSerializer,
	UserProfileUpdateSerializer,
	UserVerifyRequestSerializer,

	UserRoleCreateRequestSerializer,
	UserRoleListSerializer,

	UserPermissionCreateRequestSerializer,
	UserPermissionsListSerializer,
	UserPermissionSerializer,


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
# from libs.utils import(
# 	mail,
# 	)
from libs.exceptions import ParseException
from libs.pagination import StandardResultsSetPagination


