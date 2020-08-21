# django imports
from rest_framework import serializers

# app level imports
from .models import Candidate
from libs.helpers import time_it

class CandidateCreateRequestSerializer(serializers.Serializer):
	"""docstring for ClassName"""
	first_name = serializers.CharField(required=True)
	last_name=serializers.CharField(required=False)
	email = serializers.EmailField(required=True)
	candidate_url = serializers.CharField(required=False)
	mobile = serializers.IntegerField(required=True)
	dob=serializers.DateField(input_formats=['%d-%m-%Y',],required=False)
	gender=serializers.CharField(required=False)
	sslc_marks=serializers.CharField(required=False)
	puc_marks=serializers.CharField(required=False)
	bachelor_degree=serializers.CharField(required=False)
	bachelor_degree_course=serializers.CharField(required=False)
	bachelor_degree_marks=serializers.CharField(required=False)
	master_degree=serializers.CharField(required=False)
	master_degree_course=serializers.CharField(required=False)
	master_degree_marks=serializers.CharField(required=False)
	address = serializers.CharField(required=False)
	tech_skills= serializers.CharField(required=False)
	prefered_location=serializers.JSONField(required=False)
	previous_company=serializers.CharField(required=False)
	work_experience=serializers.CharField(required=False)
	current_ctc=serializers.FloatField(default=0.0,required=False)
	expected_ctc=serializers.FloatField(default=0.0,required=False)
	notice_period=serializers.CharField(required=False)
	resume=serializers.FileField(required=False)
	
	status = serializers.CharField(required=False)

	class Meta:
		model = Candidate
		fields = ('first_name','last_name','email ','candidate_url',
		'mobile','dob','gender','sslc_marks','puc_marks','puc_per','bachelor_degree',
		'bachelor_degree_course','bachelor_degree_marks','master_degree','master_degree_course','master_degree_marks',
		'address','tech_skills','prefered_location','previous_company','work_experience','current_ctc'
		'expected_ctc','notice_period','resume','status')        

	def create(self, validated_data):
		candidate= Candidate.objects.create(**validated_data)

		# user.set_password(validated_data['password'])

		return candidate


class CandidateListSerializer(serializers.ModelSerializer):
	"""
	"""
	class Meta:
		model=Candidate

		fields= '__all__'  





class CandidateUpdateSerializer(serializers.ModelSerializer):
	id = serializers.CharField(required=True)
	first_name = serializers.CharField(required=True)
	last_name=serializers.CharField(required=False)
	email = serializers.EmailField(required=True)
	candidate_url = serializers.CharField(required=False)
	mobile = serializers.IntegerField(required=True)
	dob=serializers.DateField(input_formats=['%d-%m-%Y',],required=False)
	gender=serializers.CharField(required=False)
	sslc_marks=serializers.CharField(required=False)
	puc_marks=serializers.CharField(required=False)
	bachelor_degree=serializers.CharField(required=False)
	bachelor_degree_course=serializers.CharField(required=False)
	bachelor_degree_marks=serializers.CharField(required=False)
	master_degree=serializers.CharField(required=False)
	master_degree_course=serializers.CharField(required=False)
	master_degree_marks=serializers.CharField(required=False)
	address = serializers.CharField(required=False)
	tech_skills= serializers.CharField(required=False)
	prefered_location=serializers.JSONField(required=False)
	previous_company=serializers.CharField(required=False)
	work_experience=serializers.CharField(required=False)
	current_ctc=serializers.FloatField(default=0.0,required=False)
	expected_ctc=serializers.FloatField(default=0.0,required=False)
	notice_period=serializers.CharField(required=False)
	resume=serializers.FileField(required=False)
	
	status = serializers.CharField(required=False)

	def update(self,instance,validated_data):


		for attr ,value in validated_data.items():
			setattr(instance,attr,value)
		instance.save()
		return instance

	class Meta:
		"""docstring for Meta"""
		model=Candidate
		fields='__all__'

class CandidateSkillsDrowpdownGetSerializer(serializers.Serializer):
    candidate_id =serializers.CharField(source='id',required=True,min_length=2)
    value = serializers.CharField(source='tech_skills',required=True, min_length=2)
    label = serializers.CharField(source='tech_skills',required=True, min_length=2)
    
    class Meta:
        model = Candidate
        fields = ('candidate_id','value','label')		
			
		
			

class DownloadResumeSerializer(serializers.ModelSerializer):
	"""docstring for DownloadResumeSerializer"""
	class Meta:
		model=Candidate
		fields=['Resume']


		
		