from rest_framework import serializers

# app level imports
from .models import Interview ,InterviewRound,InterviewStatus
from libs.helpers import time_it

from clients.models import Client
from jobs.models import Job
from candidate.models import Candidate
# from interview.models import Interview,InterviewRound,InterviewStatus
from accounts.models import User




#interview serializer
class InterviewCreateRequestSerializer(serializers.Serializer):
    date = serializers.DateField(input_formats=['%d-%m-%Y',],required=True)
    location = serializers.CharField(required=False)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(),required=True)
    job=serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(),required=True)
    interview_round=serializers.PrimaryKeyRelatedField(queryset=InterviewRound.objects.all(),required=True)
    candidate=serializers.SlugRelatedField(queryset=Candidate.objects.all(),required=False,slug_field="email")
    
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=True)
    interview_status=serializers.PrimaryKeyRelatedField(queryset=InterviewStatus.objects.all(),required=False)




    # password = serializers.CharField(required=True, min_length=5)
    class Meta:
        model = Interview
        fields = ('id','client', 'job', 'interview_round', 'candidate', 'user',
            'date', 'location', 'interview_status'
        )

    def create(self, validated_data):
        interview= Interview.objects.create(**validated_data)

        # user.set_password(validated_data['password'])
        # interview.save()

        return interview

class ClientGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        
        fields = ('id','name')
        
class JobGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'client_id', 'job_title',)

class CandidateGetSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name) 

    class Meta:
        model = Candidate
        fields= ('full_name','email','mobile') 

class UserGetSerializer(serializers.ModelSerializer):

	# full_name = serializers.SerializerMethodField()

	# def get_full_name(self, obj):
 #        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:

        model = User
        # fields ='__all__'
        fields= ('id','full_name')

class InterviewRoundGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= InterviewRound
        fields= ('id','interview_round')

class InterviewStatusGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= InterviewStatus
        fields= ('id','status')

 

class InterviewListSerializer(serializers.ModelSerializer):


    client = ClientGetSerializer()
    job = JobGetSerializer()
    candidate = CandidateGetSerializer()
    user = UserGetSerializer()
    interview_round=InterviewRoundGetSerializer()
    interview_status=InterviewStatusGetSerializer()

    class Meta:
        model = Interview
        # fields='__all__'
        
        fields = (

          'id','client','job','user','candidate',
          'interview_round','interview_status','date','location'
        )

        #   'id','client','job','user','candidate',
        #   'interview_round','interview_status','date','location'
        # )
###################################################################################
class InterviewUpdateSerilaizer(serializers.ModelSerializer):
    id=serializers.CharField(required=True)
    date = serializers.DateField(input_formats=['%d-%m-%Y',],required=True)
    location = serializers.CharField(required=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(),required=True)
    job=serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(),required=True)
    interview_round=serializers.PrimaryKeyRelatedField(queryset=InterviewRound.objects.all(),required=True)
    candidate=serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all(),required=True)
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=True)
    interview_status=serializers.PrimaryKeyRelatedField(queryset=InterviewStatus.objects.all(),required=False)

    # expiring_on = serializers.DateTimeField(required=False)

    def update(self, instance, validated_data):
        for attr ,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance

    class Meta:
        model = Interview
        # fields = ('id','date','location','interview_round','interview_status')
        fields='__all__'

        
        

#########################################################################




# inetrview_round serializer
class InterviewRoundRequestSerializer(serializers.Serializer):
    interview_round=serializers.CharField(required=True)

    class Meta:
        model = InterviewRound
        fields = '__all__'


    def create(self, validated_data):
        interview_round= InterviewRound.objects.create(**validated_data)
        interview_round.save()
        return interview_round

# class InterviewRoundListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InterviewRound
#         fields= '__all__'
class InterviewRoundListSerializer(serializers.ModelSerializer):
    class Meta:
        model= InterviewRound
        fields = '__all__'


class InterviewRoundDrowpdownGetSerializer(serializers.Serializer):
    value = serializers.CharField(source='interview_round',required=True, min_length=2)
    label = serializers.CharField(source='interview_round',required=True, min_length=2)
    interview_round_id=serializers.CharField(source='id',required=True)

    class Meta:
        model = InterviewRound
        fields = ('interview_round_id','value','label')

        


############################################################################





#interview status serializer
class InterviewStatusRequestSerializer(serializers.Serializer):
    status=serializers.CharField(required=True)

    class Meta:
        models = InterviewStatus
        fields = '__all__'


    def create(self, validated_data):
        interview_status= InterviewStatus.objects.create(**validated_data)
        interview_status.save()
        return interview_status


class InterviewStatusDrowpdownGetSerializer(serializers.Serializer):
	value = serializers.CharField(source='status',required=True, min_length=2)
	label = serializers.CharField(source='status',required=True, min_length=2)
	interview_status_id=serializers.CharField(source='id',required=True)

	class Meta:
		model = InterviewStatus
		fields = ('interview_status_id','value','label')

class InterviewStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model= InterviewStatus
        fields= '__all__'