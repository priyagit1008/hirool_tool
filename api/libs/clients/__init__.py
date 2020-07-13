# django imports
from django.conf import settings

# app level imports
from .sms import SmsClient
from .elasticsearch import MyElasticsearch
from .redis import MyRedisClient


AWS_CONFIG = settings.AWS_CONFIG['S3']


sms_client = SmsClient()
es_client = MyElasticsearch()
redis_client = MyRedisClient()
# s3_client = S3Client(
#     AWS_CONFIG['ACCESS_KEY'],
#     AWS_CONFIG['SECRET_KEY'],
#     AWS_CONFIG['REGION'],
# )
