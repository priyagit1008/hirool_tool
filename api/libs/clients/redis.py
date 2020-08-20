# python imports
import redis
import logging
# import time

# django imports
from django.conf import settings

HOST = settings.REDIS_CONFIG['HOST']
PORT = settings.REDIS_CONFIG['PORT']
DB = settings.REDIS_CONFIG['DB']
PASSWORD = settings.REDIS_CONFIG['PASSWORD']

logger = logging.getLogger(__name__)


class MyRedisClient(object):
	"""
	Redis client for Leads app
	"""
	def __init__(self, host=HOST, port=PORT, db=DB, password=PASSWORD):
		"""
		Init of redis client
		"""
		pool = redis.ConnectionPool(
			socket_timeout=10,
			socket_connect_timeout=10,
			host=host,
			port=port,
			db=db,
			password=password,
			decode_responses=True,
		)
		self.client = redis.Redis(connection_pool=pool)


	def store_data(self,key,data):
		# try:
		# 	self.client.hmset(key, data)
		# except redis.exceptions.RedisError:
		# 	logger.error("Redis: stored data ", exc_info=True)



		try:
		    self.client.set(key,data)
		    logger.info("Mail Sent ")
		    return True
		except:
		    logger.error("Redis: store_data RedisError ", exc_info=True)
		    return False


	def remove_data(self, hash_key, field):
		"""
		Remove field from hash_key - HDEL
		"""

		try:
			self.client.hdel(key,field)
		except redis.exceptions.RedisError:
			logger.error("Redis: remove_data RedisError ", exc_info=True)


	def get_Key_data(self,key):
		try:
			return self.client.get(key) 
		except:
			logger.error("Getting data from redis is failed", exc_info=True)

	def delete_Key_data(self,key):
		try:
			self.client.delete(key)
			return True
		except:
			logger.error("Dleleting data is failed", exc_info=True)

	def key_exists(self,key):
		try:
			return self.client.exists(key)
		except:
			logger.error("redis connection Failed", exc_info=True)


			