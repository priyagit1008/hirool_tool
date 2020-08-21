# django imports
from rest_framework import serializers

# app level imports
from .models import Client, Job
from libs.helpers import time_it


class ClientCreateRequestSerializer(serializers.Serializer):
    """
    ClientCreateRequestSerializer
    """
    name = serializers.CharField(required=True)
    web_link = serializers.CharField(required=True)
    ceo= serializers.CharField(required=False)
    founder= serializers.CharField(required=False)
    founded_on= serializers.CharField(required=False)
    email= serializers.CharField(required=True)
    mobile= serializers.CharField(required=True)
    revenue= serializers.CharField(required=False)
    latest_funding= serializers.CharField(required=False)
    headquarter = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    profile_desc= serializers.CharField(required=False)
    aggrement_doc= serializers.CharField(required=False)
    status= serializers.CharField(required=False)
    industry= serializers.CharField(required=False)
    category= serializers.CharField(required=False)
    

    # password = serializers.CharField(required=True, min_length=5)
    class Meta:
        model = Client
        fields = (
            'id','name', 'web_link', 'headquarter', 'address', 'industry','category',
            'business_type', 'status', 'profile_desc', 'aggrement_doc',
            'extra'
        )

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)

        # user.set_password(validated_data['password'])
        client.save()

        return client


class ClientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        # Tuple of serialized model fields (see link [2])
        fields = '__all__'
       

class ClientDrowpdownGetSerializer(serializers.Serializer):
    client_id =serializers.CharField(source='id',required=True,min_length=2)
    value = serializers.CharField(source='name',required=True, min_length=2)
    label = serializers.CharField(source='name',required=True, min_length=2)
    
    class Meta:
        model = Client
        fields = ('client_id','value','label')
        


class ClientUpdateSerializer(serializers.ModelSerializer):
    """docstring for ClientUpdateSerializer"""
    id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    web_link = serializers.CharField(required=True)
    ceo= serializers.CharField(required=False)
    founder= serializers.CharField(required=False)
    founded_on= serializers.CharField(required=False)
    email= serializers.CharField(required=True)
    mobile= serializers.CharField(required=True)
    revenue= serializers.CharField(required=False)
    latest_funding= serializers.CharField(required=False)
    headquarter = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    profile_desc= serializers.CharField(required=False)
    aggrement_doc= serializers.CharField(required=False)
    status= serializers.CharField(required=False)
    industry= serializers.CharField(required=False)
    category= serializers.CharField(required=False)
    

    def update(self, instance, validated_data):


        for attr ,value in validated_data.items():
            setattr(instance,attr,value)
            
        instance.save()
        return instance

    class Meta:
        model = Client

        fields = '__all__'




class JobCreateRequestSerializer(serializers.Serializer):
    """
    ClientCreateRequestSerializer
    """
    client_id = serializers.CharField(required=True)
    job_title = serializers.CharField(required=True)
    jd_url = serializers.CharField(required=False)
    tech_skills = serializers.JSONField(required=False)
    job_location = serializers.CharField(required=False)
    job_type = serializers.CharField(required=False)
    min_exp = serializers.IntegerField(required=False)
    max_exp = serializers.IntegerField(required=False)
    min_notice_period = serializers.IntegerField(required=False)
    max_notice_period = serializers.IntegerField(required=False)
    # status = serializers.CharField(required=False)
    min_ctc = serializers.FloatField(required=False)
    max_ctc = serializers.FloatField(required=False)

    qualification = serializers.CharField(required=False)
    percentage_criteria=serializers.IntegerField(required=False)
    status=serializers.CharField(required=False)
    jd_extra = serializers.JSONField(required=False)

    # password = serializers.CharField(required=True, min_length=5)
    class Meta:
        model = Job
        fields = (
            'client_id', 'job_title', 'jd_url', 'tech_skills', 'job_location', 'job_type',
            'min_exp', 'max_exp', 'min_notice_period', 'max_notice_period', 'min_ctc', 'max_ctc',
            'qualification','percentage_criteria','status','jd_extra'
        )

    def create(self, validated_data):
        job_obj = Job.objects.create(**validated_data)
        # client_obj = Client.objects.get(validated_data['client'])
        # job_obj.client = client_obj
        print(job_obj)
        job_obj.save()
        return job_obj

class clientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields= ('name','email','mobile','ceo','address') 

class JobGetSerializer(serializers.ModelSerializer):
    client=clientGetSerializer()
    class Meta:
        model =Job
        fields=('id','client', 'job_title', 'jd_url', 'tech_skills', 'job_location', 'job_type',
            'min_exp', 'max_exp', 'min_notice_period', 'max_notice_period', 'min_ctc', 'max_ctc',
            'qualification','percentage_criteria','status','jd_extra'
            )


class JobListSerializer(serializers.ModelSerializer):
    client=clientGetSerializer()

    class Meta:
        model = Job
        # fields = '__all__'
        # Tuple of serialized model fields (see link [2])

        fields = (
          'id','client', 'job_title', 'jd_url', 'tech_skills', 'job_location', 'job_type',
            'min_exp', 'max_exp', 'min_notice_period', 'max_notice_period', 'min_ctc', 'max_ctc',
            'qualification','percentage_criteria','status','jd_extra'
       
        )

   
        # read_only_fields = ('id',)


class JobDrowpdownGetSerializer(serializers.Serializer):
    Job_id =serializers.CharField(source='id',required=True,min_length=2)
    value = serializers.CharField(source='job_title',required=True, min_length=2)
    label = serializers.CharField(source='job_title',required=True, min_length=2)
    
    class Meta:
        model = Client
        fields = ('Job_id','value','label')

class JobUpdateSerilaizer(serializers.ModelSerializer):
    """docstring for JobUpdateSerilaizer"""
    id = serializers.CharField(required=True)

    client= serializers.CharField(required=False)
    job_title = serializers.CharField(required=True)
    jd_url = serializers.CharField(required=False)
    tech_skills = serializers.JSONField(required=False)
    job_location = serializers.CharField(required=False)
    job_type = serializers.CharField(required=False)
    min_exp = serializers.IntegerField(required=False)
    max_exp = serializers.IntegerField(required=False)
    min_notice_period = serializers.IntegerField(required=False)
    max_notice_period = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
    min_ctc = serializers.FloatField(required=False)
    max_ctc = serializers.FloatField(required=False)

    qualification = serializers.CharField(required=False)
    percentage_criteria=serializers.IntegerField(required=False)
    status=serializers.CharField(required=False)
    jd_extra = serializers.JSONField(required=False)


    def update(self, instance, validated_data):

        for attr ,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
    

    class Meta:
        model = Job
    
        fields = '__all__'
        
        
        
        




