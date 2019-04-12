import time
import logging
from flask.views import MethodView

from .models import User, Token
logger = logging.getLogger(__name__)


class CheckLogin(MethodView):
    # for the other interface check is login or not
    def get(self):
        user_id = Token.objects().first()
        logger.info("redis-check-login", user_id)
        try:
            if user_id is None:
                data = BaseResponse()
                data.error = 'redirect login'
                data.code = 400
                raise ValueError("redirect login")
                # return redirect("/api/v1/login")
            else:
                return user_id.token
        except Exception as e:
            logger.error('utils:checklogin', e)
            raise ValueError("checklogin was wrong")


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
    try:
        for index, item_gender in enumerate(li_gender):
            if arg == index:
                return item_gender
    except Exception as e:
        logger.error('utils:get-gender', e)
        raise ValueError(str(e))


def get_salary(arg):
    li_salary = ["<2000", '2000-5000', '5000-8000', '8000-10000', '10000<']
    try:
        for index, item_salary in enumerate(li_salary):
            if arg == index:
                return item_salary
    except Exception as e:
        logger.error("utils:get-salary", e)
        raise ValueError(str(e))


def get_time_format(arg):
    """
    exchange the format of the time
    :param arg: str of time
    :return: timestamp
    """
    try:
        format_time_str = time.strptime(arg, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.error('utils:get-time-format', e)
        try:
            struct_time = time.strptime(arg, "%Y-%m-%d")
            return time.mktime(struct_time)
        except Exception as e:
            logger.error("utils:get-time-format", e)
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
        logger.error('utils:get-str-time', e)
        raise ValueError(str(e))
    return time.strftime("%Y-%m-%d %H:%M:%S", struct_time)


def get_username(arg):
    """
    user_obj_id turn into username
    :param arg: User object id
    :return: username from User
    """
    try:
        user_obj = User.objects(id=arg).only('username').exclude('id')
    except Exception as e:
        logger.error('utils:get-username', e)
        raise ValueError(e)
    return user_obj[0]['username']