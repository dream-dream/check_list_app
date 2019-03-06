from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from bill_count_app.models import User, UserDetail, BillDetail
from bill_count_app.form import RegisterForm
# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user_object = User.objects.filter(username=username, pwd=password).first()
        if user_object:
            redirect('input/')
        else:
            finally_response_data = {"code": 500, "msg": "sorry, login failed, please try again"}
            return JsonResponse(finally_response_data)
    else:
        redirect('login/')


def register(request):
    finally_response_data = {"code": 500, "msg": "注册失败，请重试"}
    if request.method == 'POST':
        try:
            re_form_item = RegisterForm(request.POST)
        except Exception as e:
            print(str(e))
            return JsonResponse(finally_response_data)
        if re_form_item.is_valid():
            try:
                username = re_form_item.cleaned_data['username']
                mobile = re_form_item.cleaned_data['phone_num']
                password = re_form_item.cleaned_data['password']
                gender = re_form_item.cleaned_data['gender']
                age = re_form_item.cleaned_data['age']
                job = re_form_item.cleaned_data['job']
                salary = re_form_item.cleaned_data['salary']
                user_object = User.objects.create(username=username, phone_num=mobile, pwd=password)
                user_detail_obj = UserDetail.objects.create(gender=gender, age=age, job=job, salary=salary)
                user_object.save()
                user_detail_obj.save()
                finally_response_data["code"] = 200
                finally_response_data["msg"] = "congratulations! you register successfully"
                return JsonResponse(finally_response_data)
            except Exception as e:
                print(str(e))
                return JsonResponse(finally_response_data)

        else:
            return JsonResponse(finally_response_data)


class Input(object):
    ...


class ListOfBill(object):
    ...


class ListDetailOfBill(object):
    ...
