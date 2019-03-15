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

l = [123, '123']
obj = '123'
for i in l:
    if obj == i:
        print(l.index(i))