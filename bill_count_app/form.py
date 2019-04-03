import time
from django.shortcuts import HttpResponse, redirect


# from rest_framework.views import APIView
class BaseResponse():
    def __init__(self, code=200, data=None, error=None, *args, **kwargs):
        self.code = code
        self.data = data
        self.error = error

    @property
    def dict(self):
        return self.__dict__


def get_gender(arg):
    li_gender = ["female", "male"]
    for index, item_gender in enumerate(li_gender):
        if arg == index:
            return item_gender


def get_salary(arg):
    li_salary = ["<2000", '2000-5000', '5000-8000', '8000-10000', '10000<']
    for index, item_salary in enumerate(li_salary):
        if arg == index:
            return item_salary


def get_time_format(arg):
    """
    exchange the format of the time
    :param arg: str of time
    :return: timestamp
    """
    try:
        format_time_str = time.strptime(arg, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            struct_time = time.strptime(arg, "%Y-%m-%d")
            return time.mktime(struct_time)
        except Exception as e:
            print("exception get_time_format", e)
            return ""
    return time.mktime(format_time_str)


def get_end_back_time(arg):
    """
    timestamp turn into time string
    :param arg:
    :return:
    """
    try:
        struct_time = time.localtime(arg)
    except Exception as e:
        print("exception get_str_time", e)
        return HttpResponse(str(e))
    return time.strftime("%Y-%m-%d %H:%M:%S", struct_time)