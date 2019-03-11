from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q
import re
from bill_count_app.models import User, UserDetail, BillDetail
from bill_count_app.form import RegisterForm

# Create your views here.
finally_response_data = {"code": 500, "msg": "注册失败，请重试"}


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
            request.session["id"] = user_object.id
            redirect('input/')
        else:
            finally_response_data = {"code": 500, "msg": "sorry, login failed, please try again"}
            return JsonResponse(finally_response_data)
    else:
        redirect('login/')


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
        # todo checkout this field
        is_username = User.objects.filter(username=username).exists()
        if is_username:
            finally_response_data["code"] = 300
            finally_response_data["msg"] = "该用户名已存在，请重试"
            data["username"] = ""
            data["pwd"] = ""
            data["re_pwd"] = ""
            finally_response_data["data"] = data
            return JsonResponse(finally_response_data)
        if len(username) < 5 or len(username) > 15:
            finally_response_data["code"] = 305
            finally_response_data["msg"] = "用户名最少不低于5位，最多不高于15位,请重试"
            data["username"] = ""
            data["pwd"] = ""
            data["re_pwd"] = ""
            finally_response_data["data"] = data
            return JsonResponse(finally_response_data)

        # todo use re model to checkout this field
        if phone_num.isdigt():
            phone_num = re.findall('^1[345789]\d{9}$', phone_num)
            if not phone_num:
                finally_response_data["code"] = 405
                finally_response_data["msg"] = "手机号输入有误，请重试"
                data["phone_num"] = ""
                data["pwd"] = ""
                data["re_pwd"] = ""
                finally_response_data["data"] = data
                return JsonResponse(finally_response_data)
        else:
            finally_response_data["code"] = 400
            finally_response_data["msg"] = "格式不对，必须是纯数字，请重试"
            data["phone_num"] = ""
            data["pwd"] = ""
            data["re_pwd"] = ""
            finally_response_data["data"] = data
            return JsonResponse(finally_response_data)
        # todo checkout the power of pwd, got digit & character & symbol
        if pwd != re_pwd:
            finally_response_data["code"] = 410
            finally_response_data["msg"] = "两次密码不一致，请重新输入"
            data["pwd"] = ""
            data["re_pwd"] = ""
            finally_response_data["data"] = data
            return JsonResponse(finally_response_data)
        pwd = re.findall('^[a-zA-Z]\w{5,14}$', pwd)
        if not pwd:
            finally_response_data["code"] = 400
            finally_response_data["msg"] = "格式不对，以字母开头，包含数字字母下划线，最短6位，最长15位"
            data["pwd"] = ""
            data["re_pwd"] = ""
            finally_response_data["data"] = data
            return JsonResponse(finally_response_data)
        try:
            user_object = User.objects.create(username=username, phone_num=phone_num, pwd=pwd)
            user_detail_obj = UserDetail.objects.create(gender=gender, age=age, job=job, salary=salary)
            user_object.save()
            user_detail_obj.save()
        except Exception as e:
            print(str(e))
            return JsonResponse(finally_response_data)
    finally_response_data["code"] = 200
    finally_response_data["msg"] = "congratulations"
    return JsonResponse(data)
    # return redirect('input/')
        # 这里是用了forms组件，跟前端强耦合了，所以弃用
        # try:
        #     re_form_item = RegisterForm(request.POST)
        # except Exception as e:
        #     print(str(e))
        #     return JsonResponse(finally_response_data)
        # if re_form_item.is_valid():
        #     try:
        #         username = re_form_item.cleaned_data['username']
        #         mobile = re_form_item.cleaned_data['phone_num']
        #         password = re_form_item.cleaned_data['password']
        #         gender = re_form_item.cleaned_data['gender']
        #         age = re_form_item.cleaned_data['age']
        #         job = re_form_item.cleaned_data['job']
        #         salary = re_form_item.cleaned_data['salary']
        #         user_object = User.objects.create(username=username, phone_num=mobile, pwd=password)
        #         user_detail_obj = UserDetail.objects.create(gender=gender, age=age, job=job, salary=salary)
        #         user_object.save()
        #         user_detail_obj.save()
        #         finally_response_data["code"] = 200
        #         finally_response_data["msg"] = "congratulations! you register successfully"
        #         return JsonResponse(finally_response_data)
        #     except Exception as e:
        #         print(str(e))
        #         return JsonResponse(finally_response_data)
        #
        # else:
        #     return JsonResponse(finally_response_data)


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
            print(str(e))
            finally_response_data["code"] = 500
            finally_response_data["msg"] = "提交失败，请重试"
            return JsonResponse(finally_response_data)
    finally_response_data["code"] = 200
    finally_response_data["msg"] = "提交成功"
    return JsonResponse(finally_response_data)

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
            return JsonResponse("database was wrong, try again")
        detail_query_dict = {}
        detail_query_dict[user_id] = detail_query_set
        begin_num = 0
        for query_object in detail_query_set:
            begin_num += query_object.money
        detail_query_dict[sum] = begin_num
        return JsonResponse(detail_query_dict)


def get_list(request):
    """
    获取指定时间内的账单总金额，并且把每天的总额计算出来
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_id = request.session.get("id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        # get data what we want from database
        try:
            sum_query_set = BillDetail.objects.filter(user_id=user_id).filter(
                Q(
                    Q(time__gt=start_time) & Q(time__lt=end_time)
                ) |
                Q(time=start_time) | Q(time=end_time)
            ).values("time", "money")
        except Exception as e:
            print(str(e))
            return JsonResponse("database was wrong, try again")
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
        return JsonResponse(finally_data_format)

