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
# print("strftime", time_str)
time_loc = time.localtime(time_str)  # 把时间戳转换成结构化时间
lt_local_time = time.localtime(lt_time)

begin_time_str = time.gmtime(time_str)
fir_lt_time = time.gmtime(lt_time)
# print("first try", time_str-lt_time)


# subtraction_time = time.gmtime(time_str - lt_time)
# print("subtraction", subtraction_time)
# print(time_loc, type(time_loc))
# time_object = time.strftime('%Y-%m-%d %X', time_loc)  # 把结构化时间转换成便于阅读的时间字符串
# print(time_object, type(time_object))

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
object_datetime = datetime.datetime.now()
# print(object_datetime.date())
# list_dict = [{'time': '2012', 'money': 12}, {'time': '2012', 'money': 90}, {'time': '2090', 'money': 31},
#              {'time': '2090', 'money': 14}]
# dic = {}
# for item in list_dict:
#     if item['time'] not in dic:
#         dic[item['time']] = [item['money'], ]
#     else:
#         dic[item['time']].append(item['money'])
# print(dic)
# for value in dic.values():
#     begin_num = 0
#     for each_num in value:
#         begin_num += each_num
#     print(begin_num)


# list_dict = [{'time': '2012', 'money': 12}, {'time': '2012', 'money': 90}, {'time': '2090', 'money': 31},
#              {'time': '2090', 'money': 14}]
# dic = {}
# for item in list_dict:
#     if item['time'] not in dic:
#         dic[item['time']] = item['money']
#     else:
#         dic[item['time']] += item['money']
        # print(dic[item['time']])
# print(dic)
# finally_li = []
# for item in dic.items():
#     re_dic = {}
#     re_dic['time'] = item[0]
#     re_dic['money'] = item[1]
#     finally_li.append(re_dic)
# print(finally_li)
# for value in dic.values():
#     begin_num = 0
#     for each_num in value:
#         begin_num += each_num
#     print(begin_num)

# dic = {'name':'jinxin','age':20,'teacher':'egon'}
# del dic["name"]
# dic.pop('name')
# print(dic)
# print(dic.pop("name"))
#
# int_obj = ""
# if int_obj.isdigit():
#     print(int_obj)
# elif not int_obj.isdigit() and "":
#     print('int_obj',int_obj, type(int_obj))

# l = [123, '123']
# obj = '123'
# for i in l:
#     if obj == i:
#         print(l.index(i))
li = ["a", "b", "c"]
import random
import time, datetime
time_obj = datetime.datetime.now()
random_char = random.choice(
    [chr(random.randint(65, 90)), chr(random.randint(97, 122))])
# print(random_char)
start_str = ""
for i in range(5):
    provisional_str = str(random.randrange(10, 100))+random_char
    start_str += provisional_str
# print("start_str",start_str)
time_stamp = time.time()
struc_time = time.localtime(time_stamp)
strf_time_obj = time.strftime("%Y-%m-%d ||%X", struc_time)
# print("time_stamp", time_stamp, "struc_time", struc_time, "strf_time_obj", strf_time_obj)
# print(time.strftime("%Y-%m-%d %X"))  # 2019-03-19 17:52:27
# print(time.gmtime())  # time.struct_time(tm_year=2019, tm_mon=3, tm_mday=19, tm_hour=9, tm_min=52, tm_sec=27,
# # tm_wday=1, tm_yday=78, tm_isdst=0)
# print(time.mktime(time.localtime()), time.time())  # 1552989147.0 1552989147.831865
# print(time.asctime(), type(time.asctime()))  # Tue Mar 19 17:52:27 2019 <class 'str'>
print("random-str-obj", time.asctime()+start_str)
import calendar
cal = calendar.month(2016, 1)
# print("以下输出2016年1月份的日历:")
# print(cal)