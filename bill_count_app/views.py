from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q
from functools import wraps
import re
import json
import time
import logging
import random
# from django.views.decorators.csrf import csrf_exempt
from bill_count_app.models import User, UserDetail, BillDetail
from bill_count_app.form import get_salary, get_gender, get_time_format, get_str_time

# Create your views here.
logger = logging.getLogger(__name__)
finally_response_data = {"code": 500, "msg": "register failed，please try again"}


def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("id") and request.session.get("TokenStr"):
            return func(request, *args, **kwargs)
        else:
            return redirect("api/v1/login/")

    return inner


def login(request):
    """
    login
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user_object = User.objects.filter(username=username, pwd=password).first()
        if user_object:
            # set login status into session, for the other interface check is login or not
            random_char = random.choice(
                [chr(random.randint(65, 90)), chr(random.randint(97, 122))])
            start_str = ""
            for i in range(5):
                provisional_str = str(random.randrange(10, 100)) + random_char
                start_str += provisional_str
            request.session["id"] = user_object.id
            # request.set_signed_cookie("id", user_object.id, salt="qaz")
            request.session["TokenStr"] = time.asctime() + start_str
            global finally_response_data
            finally_response_data["code"] = 200
            finally_response_data["msg"] = "you are in"
            data = json.dumps(finally_response_data)
            return HttpResponse(data)
        else:
            finally_response_data = {"code": 500,
                                     "msg": "sorry, login failed, username or password was wrong, please try again"}
            data = json.dumps(finally_response_data)
            # ret = HttpResponse(data)
            # ret['Access-Control-Allow-Origin'] = '*'
            return HttpResponse(data)
    else:
        return redirect('api/v1/login/')


def register(request):
    """
    register
    :param request:
    :return:
    """
    data = {}
    if request.method == 'POST':
        username = request.POST.get("username")
        phone_num = request.POST.get("phone_num")
        pwd = request.POST.get("pwd")
        re_pwd = request.POST.get("re_pwd")
        gender = request.POST.get("gender")  # set checkbox
        age = request.POST.get("age")
        job = request.POST.get("job")
        salary = request.POST.get("salary")
        data["username"] = username
        data["phone_num"] = phone_num
        data["pwd"] = pwd
        data["re_pwd"] = re_pwd
        data["gender"] = gender
        data["age"] = age
        data["job"] = job
        data["salary"] = salary
        # todo checkout these fields
        try:
            if username is "" or phone_num is "" or pwd is "":
                data["code"] = 404
                data["msg"] = "sorry, username and telephone and password are required"
                data = json.dumps(data)
                return HttpResponse(data)

            is_username = User.objects.filter(username=username).exists()

            if is_username:
                data["code"] = 401
                data["msg"] = "the username already exist, could you try another one?"
                data["username"] = ""
                data = json.dumps(data)
                return HttpResponse(data)
            if username is not "" and (len(username) < 5 or len(username) > 15):
                data["code"] = 401
                data["msg"] = "the username at least got 5 bits,at most got 15 bits"
                data["username"] = ""
                data = json.dumps(data)
                return HttpResponse(data)
            # todo use re model to checkout the telephone field
            if phone_num.isdigit():
                phone_num_li = re.findall('^1[345789]\d{9}$', phone_num)
                phone_num = phone_num_li[0]
                if not phone_num:
                    data["code"] = 402
                    data["msg"] = "the telephone number was wrong, could you try again"
                    data["phone_num"] = ""
                    data = json.dumps(data)
                    return HttpResponse(data)
            elif not phone_num.isdigit() and "":
                data["code"] = 402
                data["msg"] = "the format of telephone number must be all digits,come on!"
                data["phone_num"] = ""
                data = json.dumps(data)
                return HttpResponse(data)
            # todo checkout the power of pwd, got digit & character & symbol
            if pwd != re_pwd:
                data["code"] = 400
                data["msg"] = "two passwords inconsistent，try again"
                data = json.dumps(data)
                return HttpResponse(data)
            pwd_li = re.findall('^[a-zA-Z]\w{5,14}$', pwd)
            pwd = pwd_li[0]
            if not pwd and "":
                data["code"] = 400
                data["msg"] = \
                    "the format was wrong，start with a letter，cantainer，at least 6 bits,at most 15 bits"
                data = json.dumps(data)
                return HttpResponse(data)
        except Exception as e:
            finally_response_data["code"] = 400
            finally_response_data["msg"] = str(e) + " some field was wrong, try again"
            data = json.dumps(finally_response_data)
            return HttpResponse(data)
        try:
            user_object = User.objects.create(username=username, phone_num=phone_num, pwd=pwd)
            user_item = UserDetail.objects.create(user_id_id=user_object.pk, gender=get_gender(gender), age=age,
                                                  job=job, salary=get_salary(salary))
        except Exception as e:
            finally_response_data["code"] = 300
            finally_response_data["msg"] = str(e) + "database failed, try again"
            data = json.dumps(finally_response_data)
            return HttpResponse(data)
    finally_response_data["code"] = 200
    finally_response_data["msg"] = "congratulations"
    data = json.dumps(finally_response_data)
    return HttpResponse(data)


@check_login
def input(request):
    """
    submit bill tips
    :param request:
    :return:
    """
    if request.method == 'POST':
        money = request.POST.get("money")
        remarks = request.POST.get("remarks")
        this_moment = float(request.POST.get("time"))  # 这里获取的是时间字符串，这样的格式比较符合预期，然后转换成时间对象或许能容易些
        user_id = request.session.get("id")
        try:
            # bill_obj = BillDetail.objects.filter(user_id_id=user_id).exists()
            # if bill_obj is False:
            #     BillDetail.objects.create(time=this_moment, money=money, remarks=remarks, user_id_id=user_id)
            BillDetail.objects.create(time=this_moment, money=money, remarks=remarks, user_id_id=user_id)
        except Exception as e:
            finally_response_data["code"] = 500
            finally_response_data["msg"] = str(e) + "database failed，try again"
            data = json.dumps(finally_response_data)
            return HttpResponse(data)
    finally_response_data["code"] = 200
    finally_response_data["msg"] = "congratulation, you wrote a bill tip"
    data = json.dumps(finally_response_data)
    return HttpResponse(data)

@check_login
def get_list(request):
    """
    get list of bill tips
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = request.session.get("id")
        start_obj = request.POST.get("start_time")
        end_obj = request.POST.get("end_time")
        start_time = get_time_format(start_obj)
        end_time = get_time_format(end_obj)
        # get data what we want from database
        try:
            sum_query_set = BillDetail.objects.filter(user_id_id=user_id,
                                                      time__range=(start_time, end_time)).values_list("time",
                                                                                                      "money").all()
        except Exception as e:
            logger.error(str(e))
            finally_response_data["code"] = 300
            finally_response_data["msg"] = str(e) + "database failed, try again"
            data = json.dumps(finally_response_data)
            return HttpResponse(data)
        finally_data_format = []
        start_num = 0
        for query_object in sum_query_set:
            sum_money_dict = {}
            sum_money_dict["time"] = get_str_time(query_object[0])
            sum_money_dict["money"] = query_object[1]
            start_num += query_object[1]
            finally_data_format.append(sum_money_dict)
        #  integrate data format
        finally_response_data["code"] = 201
        finally_response_data["msg"] = "you got what you want"
        finally_response_data["data_detail"] = finally_data_format
        finally_response_data["total_money"] = start_num
        data = json.dumps(finally_response_data)
        return HttpResponse(data)
    finally_response_data["code"] = 200
    finally_response_data["msg"] = "congratulations"
    data = json.dumps(finally_response_data)
    return HttpResponse(data)


@check_login
def get_detail(request):
    """
    get detail of bill tips
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = request.session.get("id")
        start_time = request.POST.get("start_time")
        start_time = get_time_format(start_time)
        end_time = request.POST.get("end_time")
        end_time = get_time_format(end_time)
        try:
            detail_query_set = BillDetail.objects.filter(user_id_id=user_id,
                                                         time__range=(start_time, end_time)).values_list("time",
                                                                                                         "remarks",
                                                                                                         "money").all()
        except Exception as e:
            logger.error(str(e))
            finally_response_data["code"] = 300
            finally_response_data["msg"] = str(e) + "database failed, try again"
            data = json.dumps(finally_response_data)
            return HttpResponse(data)
        detail_query_li = []
        begin_num = 0
        for query_object in detail_query_set:
            dic_inner_query = {}
            dic_inner_query["time"] = get_str_time(query_object[0])
            dic_inner_query["remarks"] = query_object[1]
            dic_inner_query["money"] = query_object[2]
            begin_num += query_object[2]
            detail_query_li.append(dic_inner_query)
        finally_response_data["code"] = 201
        finally_response_data["msg"] = "you got what you want"
        finally_response_data["data_detail"] = detail_query_li
        finally_response_data["total"] = begin_num
        data = json.dumps(finally_response_data)
        return HttpResponse(data)
    finally_response_data["code"] = 200
    finally_response_data["msg"] = "congratulations"
    data = json.dumps(finally_response_data)
    return HttpResponse(data)


@check_login
def logout(request):
    request.session.delete("id")
    request.session.delete("TokenStr")
    return redirect("login/")
