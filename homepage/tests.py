from django.test import TestCase

# Create your tests here.
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=15)
redis = redis.Redis(connection_pool=pool)

print(redis.keys())