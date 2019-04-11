"""
first i get frame,
second i get database,
finally get views, redis
"""
import time
print(time.time(), time.localtime())
import redis
# redis_obj = redis.Redis(host='localhost', port=6379, decode_responses=True)
# redis_obj.set('uuid', '5cad5ce2dc46d03aced294be')
# str_obj = redis_obj.get('uuid')
# print(str_obj, type(str_obj))