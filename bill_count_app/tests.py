from django.test import TestCase

# Create your tests here.
digit = '123'
# print(type(digit))
if digit.isdigit():
    digit = int(digit)
# print(type(digit))
import time, datetime, _strptime
time_str = time.time()  # 获取时间戳
lt_time = 155197265.092492
print("strftime", time_str)
time_loc = time.localtime(time_str)  # 把时间戳转换成结构化时间
lt_local_time = time.localtime(lt_time)

begin_time_str = time.gmtime(time_str)
fir_lt_time = time.gmtime(lt_time)
print("first try", time_str-lt_time)



subtraction_time = time.gmtime(time_str - lt_time)
print("subtraction", subtraction_time)
print(time_loc, type(time_loc))
time_object = time.strftime('%Y-%m-%d %X', time_loc)  # 把结构化时间转换成便于阅读的时间字符串
print(time_object, type(time_object))

# begin_num = 0
# for every_num in range(5):
#     begin_num = begin_num + every_num
#     # every_num += every_num
# print(begin_num)
# dict = {1:12,2:23}
# for i in range(5):
#     if i in dict:
#         pass
#     else:
#         dict[i] = 'nothing'
# print(dict)