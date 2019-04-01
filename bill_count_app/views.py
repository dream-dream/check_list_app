import re
import json
import time
import random
import logging
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from rest_framework.views import APIView

from bill_count_app.models import User, UserDetail, BillDetail
from bill_count_app.form import get_time_format, get_str_time, get_gender, get_salary, CheckLogin
from bill_count_app.serializers_rest.model_seria import UserDetailSerializer, UserSerializer, BillDetailSerializer

# Create your views here.
logger = logging.getLogger(__name__)

finally_response_data = {"code": 500, "msg": "register failed，please try again"}


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        """
        login
        :param request:
        :return:
        """
        username = request.data.get('username')
        password = request.data.get('pwd')
        user_object = User.objects.filter(username=username, pwd=password).first()
        data_dic = {}
        data_dic["username"] = username
        data_dic["pwd"] = password
        serializer = UserSerializer(data=data_dic, context={"request": request})
        if serializer.is_valid():
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
            return JsonResponse(serializer.data, status=finally_response_data)
        else:
            finally_response_data = {"code": 500,
                                     "msg": "sorry, login failed, username or password was wrong, please try again"}
            return JsonResponse(serializer.error, status=finally_response_data)


class RegisterApiView(APIView):
    def post(self, request):
        """
        register
        :param request:
        :return:
        """
        user_data = {}
        user_detail_data = {}
        username = request.data.get("username")
        phone_num = request.data.get("phone_num")
        pwd = request.data.get("pwd")
        re_pwd = request.data.get("re_pwd")
        gender = request.data.get("gender")  # set checkbox
        age = request.data.get("age")
        job = request.data.get("job")
        salary = request.data.get("salary")
        user_data["username"] = username
        user_data["phone_num"] = phone_num
        user_data["pwd"] = pwd
        user_data["re_pwd"] = re_pwd
        user_detail_data["gender"] = gender
        user_detail_data["age"] = age
        user_detail_data["job"] = job
        user_detail_data["salary"] = salary
        # todo checkout these fields
        if pwd != re_pwd:
            finally_response_data["code"] = 404
            finally_response_data["msg"] = "two passwords was different, try again"
            return JsonResponse(finally_response_data)
        user_ser = UserSerializer(data=user_data)
        user_detail_ser = UserDetailSerializer(data=user_detail_data)
        user_ser_bool = user_ser.is_valid()
        user_detail_ser_bool = user_detail_ser.is_valid()
        if user_ser_bool and user_detail_ser_bool:
            logger.info(user_ser.data, user_detail_ser.data)
            try:
                with transaction.atomic():  # rollback
                    user_object = User.objects.create(username=user_ser.data["username"],
                                                      phone_num=user_ser.data["phone_num"], pwd=user_ser.data["pwd"])
                    logger.debug("user_object", user_object)
                    user_item = UserDetail.objects.create(user_id_id=user_object.pk,
                                                          gender=user_detail_ser.data["gender"],
                                                          age=user_detail_ser.data["age"],
                                                          job=user_detail_ser.data["job"],
                                                          salary=user_detail_ser.data["salary"])
            except Exception as e:
                finally_response_data["code"] = 500
                finally_response_data["msg"] = str(e) + "/n database failed, try again"
                return JsonResponse(finally_response_data)
        else:
            logger.error("errors-----msg", user_ser.errors, user_detail_ser.errors, "end--msg")
            finally_response_data["code"] = 500
            finally_response_data["msg"] = "is_valid failed, checkout errors"
            return JsonResponse(finally_response_data)
        for item in user_ser.data.items():
            finally_response_data[item[0]] = item[1]
        for item in user_detail_ser.data.items():
            if item[0] == "salary":
                finally_response_data[item[0]] = get_salary(item[1])
            elif item[0] == "gender":
                finally_response_data[item[0]] = get_gender(item[1])
            else:
                finally_response_data[item[0]] = item[1]
        finally_response_data["code"] = 200
        finally_response_data["msg"] = "congratulations"
        return JsonResponse(finally_response_data)


class BillApiView(APIView):
    def post(self, request):
        """
        submit bill tips
        :param request:
        :return:
        """
        money = request.data.get("money")
        remarks = request.data.get("remarks")
        this_moment = float(request.data.get("time"))  # 这里获取的是时间字符串，这样的格式比较符合预期，然后转换成时间对象或许能容易些
        user_id = CheckLogin.check
        try:
            bill_obj = BillDetail.objects.create(time=this_moment, money=money, remarks=remarks, user_id_id=user_id)
            bill_serializer = BillDetailSerializer(data=bill_obj, context={"request": request})
        except Exception as e:
            finally_response_data["code"] = 500
            finally_response_data["msg"] = str(e) + "database failed，try again"
            return JsonResponse(bill_serializer.errors, status=finally_response_data)
        finally_response_data["code"] = 200
        finally_response_data["msg"] = "congratulation, you wrote a bill tip"
        return JsonResponse(bill_serializer.data.dict, status=finally_response_data)

    def get(self, request):
        """
        get list of bill tips
        :param request:
        :return:
        """
        user_id = CheckLogin.check
        start_obj = request.data.get("start_time")
        end_obj = request.data.get("end_time")
        start_time = get_time_format(start_obj)
        end_time = get_time_format(end_obj)
        # get data what we want from database
        try:
            sum_query_set = BillDetail.objects.filter(user_id_id=user_id,
                                                      time__range=(start_time, end_time)).values_list("time", "money",
                                                                                                      "remarks").all()
            bill_detail_serializer = BillDetailSerializer(data=sum_query_set, context={"request": request})
        except Exception as e:
            logger.error(str(e))
            finally_response_data["code"] = 300
            finally_response_data["msg"] = str(e) + "database failed, try again"
            return JsonResponse(bill_detail_serializer.errors, status=finally_response_data)
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
            return JsonResponse(finally_response_data)
        finally_response_data["code"] = 200
        finally_response_data["msg"] = "congratulations"
        return JsonResponse(bill_detail_serializer.data, status=finally_response_data)

    # def get_detail(self, request):
    #     """
    #     get detail of bill tips
    #     :param request:
    #     :return:
    #     """
    #
    #     user_id = request.session.get("id")
    #     start_time = request.POST.get("start_time")
    #     start_time = get_time_format(start_time)
    #     end_time = request.POST.get("end_time")
    #     end_time = get_time_format(end_time)
    #     try:
    #         detail_query_set = BillDetail.objects.filter(user_id_id=user_id,
    #                                                      time__range=(start_time, end_time)).values_list("time",
    #                                                                                                      "remarks",
    #                                                                                                      "money").all()
    #     except Exception as e:
    #         logger.error(str(e))
    #         finally_response_data["code"] = 300
    #         finally_response_data["msg"] = str(e) + "database failed, try again"
    #         data = json.dumps(finally_response_data)
    #         return HttpResponse(data)
    #     detail_query_li = []
    #     begin_num = 0
    #     for query_object in detail_query_set:
    #         dic_inner_query = {}
    #         dic_inner_query["time"] = get_str_time(query_object[0])
    #         dic_inner_query["remarks"] = query_object[1]
    #         dic_inner_query["money"] = query_object[2]
    #         begin_num += query_object[2]
    #         detail_query_li.append(dic_inner_query)
    #     finally_response_data["code"] = 201
    #     finally_response_data["msg"] = "you got what you want"
    #     finally_response_data["data_detail"] = detail_query_li
    #     finally_response_data["total"] = begin_num
    #     data = json.dumps(finally_response_data)
    #     return HttpResponse(data)


def logout(request):
    """
    there is a bug, when you logout, you still could get all data, that couldn't happen any more
    :param request:
    :return:
    """
    user_id = CheckLogin.check
    if user_id:
        request.session.delete("id")
        request.session.delete("TokenStr")
        finally_response_data['code'] = 666
        finally_response_data['msg'] = "you are out"
        return JsonResponse(finally_response_data)
    else:
        return JsonResponse(finally_response_data)
