from django.test import TestCase

# Create your tests here.
digit = '123'
# print(type(digit))
if digit.isdigit():
    digit = int(digit)
# print(type(digit))
import time, datetime, _strptime

time_str = time.time()
lt_time = 155197265.092492
# print("strftime", time_str)
time_loc = time.localtime(time_str)  # turn timestamp to strucktime
lt_local_time = time.localtime(lt_time)

begin_time_str = time.gmtime(time_str)
fir_lt_time = time.gmtime(lt_time)
# print("first try", time_str-lt_time)


# subtraction_time = time.gmtime(time_str - lt_time)
# print("subtraction", subtraction_time)
# print(time_loc, type(time_loc))
# time_object = time.strftime('%Y-%m-%d %X', time_loc)  # turn strucktime to str time
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
    provisional_str = str(random.randrange(10, 100)) + random_char
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
# print("random-str-obj", time.asctime()+start_str)
import calendar

cal = calendar.month(2016, 1)
# print("print calendar of 2016,Jan")
# print(cal)

time_str = "2019-2-20 12:23:43"
format_time_str = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
# print(time.mktime(format_time_str))

# print(format_time_str)  # time.struct_time(tm_year=2019, tm_mon=2, tm_mday=20, tm_hour=12, tm_min=23, tm_sec=43,
# tm_wday=2, tm_yday=51, tm_isdst=-1)
# print(time.strftime("%Y-%m-%d %H:%M:%S", format_time_str))
timeStamp = 1550636623.0
# structTime = time.localtime(timeStamp)  # 2019-02-20 12:23:43
structTime = time.gmtime(timeStamp)  # 2019-02-20 04:23:43
# print(time.strftime("%Y-%m-%d %H:%M:%S", structTime))
import re

phone_num = re.findall('^1[345789]\d{9}$', "18978654454")
# print(phone_num, type(phone_num))  # ['18978654454'] <class 'list'>
search_obj = re.search('a', 'aeva egon yuan')
# print(search_obj.group())
match_obj = re.match('a', 'aeva egon yuan')
# print(match_obj.group())
findall_obj = re.findall('a', 'aeva egon yuan')
# print(findall_obj)
# print(time_stamp)  # 1553170087.56557
fore_end = 1553169361.259  # 1553169361259  strftime:"2019-03-21 19:56:01"
test_obj = 1553126400.0
# print(time_stamp < fore_end)
database_time = 1553170704.840  # timestamp from fore-end checkout
struct = time.localtime(database_time)
# print(time.strftime("%Y-%m-%d %H:%M:%S", struct))

dic_data = {"22": "a", "33": "b", 44:"q"}
for i in dic_data.items():
    # print(i, type(i))
    print(i[0], i[1])