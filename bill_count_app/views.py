from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q
import re
from bill_count_app.models import User, UserDetail, BillDetail
from bill_count_app.form import RegisterForm

# Create your views here.
finally_response_data = {"code": 500, "msg": "注册失败，请重试"}


def login(request):
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
    if request.method == 'POST':
        username = request.POST.get("username")
        # todo checkout this field
        is_username = User.objects.filter(username=username).exists()
        if is_username:
            finally_response_data["code"] = 300
            finally_response_data["msg"] = "该用户名已存在，请重试"
            return JsonResponse(finally_response_data)
        if len(username) < 5:
            finally_response_data["code"] = 305
            finally_response_data["msg"] = "用户名最少不低于5位，请重试"
            return JsonResponse(finally_response_data)
        if len(username) > 15:
            finally_response_data["code"] = 315
            finally_response_data["msg"] = "用户名最多不高于15位，请重试"
            return JsonResponse(finally_response_data)
        phone_num = request.POST.get("phone_num")
        # todo use re model to checkout this field
        if phone_num.isdigt():
            phone_num = re.findall('^1[345789]\d{9}$', phone_num)
            if not phone_num:
                finally_response_data["code"] = 405
                finally_response_data["msg"] = "手机号输入有误，请重试"
                return JsonResponse(finally_response_data)
        else:
            finally_response_data["code"] = 400
            finally_response_data["msg"] = "格式不对，必须是纯数字，请重试"
            return JsonResponse(finally_response_data)
        pwd = request.POST.get("pwd")
        re_pwd = request.POST.get("re_pwd")
        # todo checkout the power of pwd, got digit & character & symbol
        if pwd != re_pwd:
            finally_response_data["code"] = 410
            finally_response_data["msg"] = "两次密码不一致，请重新输入"
            return JsonResponse(finally_response_data)
        pwd = re.findall('^[a-zA-Z]\w{5,14}$', pwd)
        if not pwd:
            finally_response_data["code"] = 400
            finally_response_data["msg"] = "格式不对，以字母开头，包含数字字母下划线，最短6位，最长15位"
            return JsonResponse(finally_response_data)
        gender = request.POST.get("gender")  # set checkbox
        age = request.POST.get("age")  # set checkbox
        job = request.POST.get("job")
        salary = request.POST.get("salary")  # set checkbox
        try:
            user_object = User.objects.create(username=username, phone_num=phone_num, pwd=pwd)
            user_detail_obj = UserDetail.objects.create(gender=gender, age=age, job=job, salary=salary)
            user_object.save()
            user_detail_obj.save()
        except Exception as e:
            print(str(e))
            return JsonResponse(finally_response_data)
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
    if request.method == 'POST':
        money = request.POST.get("money")
        remarks = request.POST.get("remarks")
        this_moment = request.POST.get("time")
        user_id = request.session.get("id")
        try:
            bill_obj = BillDetail.objects.filter(user_id=user_id)
            bill_obj.create(time=this_moment, money=money, remarks=remarks)
        except Exception as e:
            print(str(e))
            finally_response_data["code"] = 500
            finally_response_data["msg"] = "提交失败，请重试"
            return JsonResponse(finally_response_data)


def get_detail(request):
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
    if request.method == 'GET':
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
    ...
