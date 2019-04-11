import time
from flask import jsonify
from flask.views import MethodView
from django.shortcuts import HttpResponse

from .models import User, Token


class CheckLogin(MethodView):
    def get(self):
        user_id = Token.objects().first()
        # logger.info("redis-check-login", user_id, token_str)
        if user_id is None:
            data = BaseResponse()
            data.error = 'redirect login'
            data.code = 400
            raise ValueError("redirect login")
            # return redirect("/api/v1/login")
        else:
            return user_id.token


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
            return ""
    return time.mktime(format_time_str)


def get_str_time(arg):
    """
    timestamp turn into time string
    :param arg:
    :return:
    """
    try:
        struct_time = time.localtime(arg)
    except Exception as e:
        return HttpResponse(str(e))
    return time.strftime("%Y-%m-%d %H:%M:%S", struct_time)


def get_username(arg):
    """
    user_obj_id turn into username
    :param arg: User object id
    :return: username from User
    """
    user_obj = User.objects(id=arg).only('username').exclude('id')
    return user_obj[0]['username']