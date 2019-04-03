from django.test import TestCase
import time
# Create your tests here.
from bill_count_app.form import BaseResponse

"""
fore-end translate database field such as gender, salary, 
fore-end translate time field as time-str object
method==post,logic was that,you should integrate your data format as dict and then serializer,return serializer data
method=get,one of logic was that get out data from database  as dict serializer, 
return serializer data, the other was that get out data from database integrate data and then return.
"""


def get_gender(arg):
    li_gender = ["female", "male"]
    for item_gender, index in enumerate(li_gender):
        print(item_gender, index)
        if arg == item_gender:
            return index


# get_obj = get_gender(1)
# print(get_obj)
ret = BaseResponse()
dic_obj = {"name": "paul", "gender": "male", "age": 23, "job": "lawyer"}
dic_item = {}
for item in dic_obj.items():
    key = item[0]
    dic_item[key] = item[1]
    ret.data = dic_item
# print(ret.dict)
