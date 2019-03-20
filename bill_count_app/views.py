from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q
from functools import wraps
import re
import json
import time
import random
# from django.views.decorators.csrf import csrf_exempt
from bill_count_app.models import User, UserDetail, BillDetail
from bill_count_app.form import get_salary, get_gender

# Create your views here.
finally_response_data = {"code": 500, "msg": "register failed，please try again"}


def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("id") and request.session.get("TokenStr"):
            return func(request, *args, **kwargs)
        else:
            redirect("login/")

    return inner


def login(request):
    """
    登陆
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
        redirect('login/')
    return HttpResponse("hello")


def register(request):
    """
    注册
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
            phone_num = re.findall('^1[345789]\d{9}$', phone_num)
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
        pwd = re.findall('^[a-zA-Z]\w{5,14}$', pwd)
        if not pwd and "":
            data["code"] = 400
            data["msg"] = \
                "the format was wrong，start with a letter，cantainer，at least 6 bits,at most 15 bits"
            data = json.dumps(data)
            return HttpResponse(data)

        try:
            user_object = User.objects.create(username=username, phone_num=phone_num, pwd=pwd)
            user_item = UserDetail.objects.create(user_id_id=user_object.pk, gender=get_gender(gender), age=age,
                                                  job=job, salary=get_salary(salary))
        except Exception as e:
            print("exception", str(e))
            return HttpResponse(finally_response_data)
    finally_response_data["code"] = 200
    finally_response_data["msg"] = "congratulations"
    data = json.dumps(finally_response_data)
    return HttpResponse(data)


@check_login
def input(request):
    """
    提交记账信息
    :param request:
    :return:
    """
    if request.method == 'POST':
        money = request.POST.get("money")
        remarks = request.POST.get("remarks")
        this_moment = request.POST.get("time")  # 这里获取的是时间字符串，这样的格式比较符合预期，然后转换成时间对象或许能容易些
        user_id = request.session.get("id")
        try:
            bill_obj = BillDetail.objects.filter(user_id=user_id)
            bill_obj.create(time=this_moment, money=money, remarks=remarks)
        except Exception as e:
            print('Exception', str(e))
            finally_response_data["code"] = 500
            finally_response_data["msg"] = "submit failed，try again"
            data = json.dumps(finally_response_data)
            return HttpResponse(data)
    finally_response_data["code"] = 200
    finally_response_data["msg"] = "submit successfully"
    data = json.dumps(finally_response_data)
    return HttpResponse(data)


@check_login
def get_detail(request):
    """
    获取指定时间内的账单信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_id = request.session.get("id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        try:
            detail_query_set = BillDetail.objects.filter(user_id=user_id).filter(
                Q(
                    Q(time__gt=start_time) & Q(time__lt=end_time)
                ) |
                Q(time=start_time) | Q(time=end_time)
            ).values("time", "remarks", "money")
        except Exception as e:
            print(str(e))
            return HttpResponse("database was wrong, try again")
        detail_query_dict = {}
        detail_query_dict[user_id] = detail_query_set
        begin_num = 0
        for query_object in detail_query_set:
            begin_num += query_object.money
        detail_query_dict[sum] = begin_num
        data = json.dumps(detail_query_dict)
        return HttpResponse(data)


@check_login
def get_list(request):
    """
    获取指定时间内的账单总金额，并且把每天的总额计算出来
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = request.session.get("id")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        # get data what we want from database
        try:
            sum_query_set = BillDetail.objects.filter(user_id=user_id).filter(
                Q(
                    Q(time__gt=start_time) & Q(time__lt=end_time)
                ) |
                Q(time=start_time) | Q(time=end_time)
            ).values("time", "money")
        except Exception as e:
            print("exception", str(e))
            return HttpResponse("database was wrong, try again")
        # total the money that transaction on the same day
        sum_money_dict = {}
        start_num = 0
        for query_object in sum_query_set:
            if query_object["time"].date() not in sum_money_dict:
                sum_money_dict[query_object["time"].date()] = query_object["money"]
            else:
                sum_money_dict[query_object["time"].date()] += query_object["money"]
            start_num += query_object["money"]
        #  integrate data format
        finally_data_format = []
        for item in sum_money_dict.items():
            each_dict = {}
            each_dict["time"] = item[0]
            each_dict["money"] = item[1]
            finally_data_format.append(each_dict)
        finally_data_format.append({"total_money": start_num})
        data = json.dumps(finally_response_data)
        return HttpResponse(data)
    return HttpResponse("hello there")


@check_login
def logout(request):
    request.session.delete("id")
    request.session.delete("TokenStr")
    redirect("login/")
