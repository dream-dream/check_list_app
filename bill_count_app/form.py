import time
from django.shortcuts import HttpResponse, redirect


class CheckLogin():
    def check(self, request):
        user_id = request.session.get("id")
        if user_id and request.session.get("TokenStr"):
            return user_id
        else:
            redirect("register/")


def get_gender(arg):
    li_gender = ["female", "male"]
    for item_gender in li_gender:
        if arg == item_gender:
            return li_gender.index(arg)


def get_salary(arg):
    li_salary = ["<2000", '2000-5000', '5000-8000', '8000-10000', '10000<']
    for item_salary in li_salary:
        if arg == item_salary:
            return li_salary.index(arg)


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
            return time.mktime(struct_time) * 1000
        except Exception as e:
            print("exception get_time_format", e)
            return ""
    return time.mktime(format_time_str) * 1000


def get_str_time(arg):
    division_obj = arg / 1000
    try:
        struct_time = time.localtime(division_obj)
    except Exception as e:
        print("exception get_str_time", e)
        return HttpResponse(str(e))
    return time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
