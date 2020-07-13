import unicodedata
import os,io
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template.loader import render_to_string
import json 
# import win32com.client as client



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
from accounts.users.permissions import HiroolReadOnly,HiroolReadWrite
from .serializers import (
	CandidateCreateRequestSerializer,
	CandidateListSerializer,
	CandidateListSerializer,
	CandidateUpdateSerializer,
	# CandidateDropdownListSerializer,
	)
from .services import CandidateServices
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
		
)
from libs import (
				# redis_client,
				otpgenerate,
				mail,
				)
from api.default_settings import MEDIA_ROOT 

from libs.exceptions import ParseException
import codecs 

# Create your views here.

class CandidateViewSet(GenericViewSet):
	"""docstring for candidateViewset"""
	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = CandidateServices()
	filter_backends = (filters.OrderingFilter,)
	parser_class = (FileUploadParser,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict={
			'candidate':CandidateCreateRequestSerializer,
			'candidate_list':CandidateListSerializer,
			'candidate_get':CandidateListSerializer,
			'candidate_update':CandidateUpdateSerializer,
			# 'candidate_dropdown':CandidateDropdownListSerializer,
			}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,],)
	def candidate(self,request):
		"""
		Returns candidate account creation
		"""
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			print(serializer.errors)

			raise ParseException({'status':'Incorrect Input'}, serializer.errors)

		if Candidate.objects.filter(email=self.request.data['email']).exists():
			return Response({"status":"candidate already exists"},status=status.HTTP_400_BAD_REQUEST)

		print("create candidate with", serializer.validated_data)
		candidate= serializer.create(serializer.validated_data)

		if candidate:

			# msg_plain = render_to_string('email_message.txt',{"user":candidate.first_name})
			# msg_html = render_to_string('email.html',{"user":candidate.first_name})
			# send_mail('Hirool',msg_plain,settings.EMAIL_HOST_USER,[candidate.email],html_message=msg_html,)

			return Response({'status':'Successfully added'},status=status.HTTP_201_CREATED)
		return Response({"status": "Not Found"},status.HTTP_404_NOT_FOUND) 


		
	
	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def candidate_list(self,request,**dict):
		"""
		Returns candidate list
		"""
		try:
			filter_data=request.query_params.dict()
			serializer=self.get_serializer(self.services.get_queryset_service(filter_data), many=True)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)



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
			raise
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
				print(serializer.errors)
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()    
				return Response({"status":"updated Successfully"},status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def candidate_dropdown(self,request):
		"""
		Returns single candidate details
		"""
		try:
			id= request.GET.get('id', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.get_candidate_service(id))
				return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(
		methods=['get'],
		detail= False,
		permission_classes=[IsAuthenticated,],
		)
	def download_file(self,request, encoding='utf8'):
		"""
		Download candidate resume
		"""
		try:   
			id=request.GET["id"]
			print(id)
			resume_name = Candidate.objects.get(id=id).resume
			print(resume_name)
			resume_path = os.path.join(MEDIA_ROOT,str(resume_name))
			print(resume_path)
			FilePointer = open(resume_path,'rb')
			print(FilePointer)
			response = HttpResponse((FilePointer),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
			print(response)
			response['Content-Disposition'] = 'attachment; filename="%s.docx"' %(resume_name)
			return response
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	# @action(
	# 	methods=['get'],
	# 	detail= False,
	# 	permission_classes=[],)
	# def convert_to_pdf(filepath:str):
 #    """Save a pdf of a docx file."""    
 #    try:
 #        word = client.DispatchEx("Word.Application")
 #        target_path = filepath.replace(".docx", r".pdf")
 #        word_doc = word.Documents.Open(filepath)
 #        word_doc.SaveAs(target_path, FileFormat=17)
 #        word_doc.Close()
 #    except Exception as e:
 #            raise e
 #    finally:
 #            word.Quit()
	


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def candidate_columns(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/candidate_columns.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		print("hi")
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

	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def prepared_location(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/prepared_location.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		print("hi")
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
