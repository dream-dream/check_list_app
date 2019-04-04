import re
import json
import redis
import time
import random
import logging
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.views import APIView

from bill_count_app.models import User, UserDetail, BillDetail
from bill_count_app.form import get_time_format, get_gender, get_salary, get_end_back_time, \
    BaseResponse
from bill_count_app.serializers_rest.model_seria import UserDetailSerializer, RegisterSerializer, BillInputSerializer, \
    BillDetailSerializer

# Create your views here.
logger = logging.getLogger(__name__)
# put login user id in redis
redis_con = redis.ConnectionPool(host="127.0.0.1", port=6379)
redis_obj = redis.Redis(connection_pool=redis_con)


class CheckLogin(APIView):
    def get(self, request):
        user_id = redis_obj.get("id")
        token_str = redis_obj.get("TokenStr")
        logger.info("redis-check-login", user_id, token_str)
        if user_id and token_str:
            return user_id
        else:
            redirect("login/")


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        """
        login
        :param request:
        :return:
        """
        final_data = BaseResponse()
        username = request.data.get('username')
        password = request.data.get('pwd')
        user_object = User.objects.filter(username=username, pwd=password).first()
        if user_object:
            # set login status into session, for the other interface check is login or not
            random_char = random.choice(
                [chr(random.randint(65, 90)), chr(random.randint(97, 122))])
            start_str = ""
            for i in range(5):
                provisional_str = str(random.randrange(10, 100)) + random_char
                start_str += provisional_str
            redis_obj.set("id", user_object.id)
            redis_obj.set("TokenStr", time.asctime() + start_str)
            final_data.code = 200
            final_data.data = "you are in"
            final_data.username = username
            final_data.password = password
            final_data.token = request.session["TokenStr"]
            return JsonResponse(final_data.dict)
        else:
            final_data.code = 500
            final_data.data = "sorry, login failed, username or password was wrong, please try again"
            logger.error(final_data)
            return JsonResponse(final_data.dict)


class RegisterApiView(APIView):
    def post(self, request):
        """
        register
        :param request:
        :return:
        """
        final_data = BaseResponse()
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
            final_data.code = 404
            final_data.data = "two passwords was different, try again"
            return JsonResponse(final_data.dict)
        user_ser = RegisterSerializer(data=user_data)
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
                    UserDetail.objects.create(user_id_id=user_object.pk,
                                              gender=user_detail_ser.data["gender"],
                                              age=user_detail_ser.data["age"],
                                              job=user_detail_ser.data["job"],
                                              salary=user_detail_ser.data["salary"])
            except Exception as e:
                final_data.code = 500
                final_data.data = str(e) + "/n database failed, try again"
                return JsonResponse(final_data.dict)
        else:
            logger.error("errors-----msg", user_ser.errors, user_detail_ser.errors, "end--msg")
            final_data.code = 500
            final_data.data = "is_valid failed, checkout errors"
            return JsonResponse(final_data.dict)
        data_dic = {}
        for item in user_ser.data.items():
            data_dic[item[0]] = item[1]
        for item in user_detail_ser.data.items():
            key_obj = item[0]
            if key_obj == "salary":
                data_dic[key_obj] = get_salary(item[1])
            elif key_obj == "gender":
                data_dic[key_obj] = get_gender(item[1])
            else:
                data_dic[key_obj] = item[1]
        final_data.code = 200
        final_data.data = data_dic
        print("final-dict", final_data.dict)
        return JsonResponse(final_data.dict)


class BillApiView(CheckLogin):
    def post(self, request):
        """
        submit bill tips
        :param request:
        :return:
        """
        final_data = BaseResponse()
        money = request.data.get("money")
        remarks = request.data.get("remarks")
        this_moment = time.time()
        user_id = redis_obj.get("id")
        data_dic = {}
        data_dic["money"] = money
        data_dic["remarks"] = remarks
        data_dic["time"] = this_moment
        data_dic["user_id"] = user_id
        bill_serializer = BillInputSerializer(data=data_dic)
        logger.info("serializer", bill_serializer)
        bill_ser_bool = bill_serializer.is_valid()
        if bill_ser_bool:
            try:
                BillDetail.objects.create(time=this_moment, money=money, remarks=remarks, user_id_id=user_id)
            except Exception as e:
                final_data.code = 500
                final_data.data = str(e) + "database failed，try again"
                logger.error(bill_serializer.errors, final_data.dict)
                return JsonResponse(final_data.dict)
        else:
            logger.error("errors-----msg", bill_serializer.errors, "end--msg")
            final_data.code = 500
            final_data.data = "is_valid failed, checkout errors"
            return JsonResponse(final_data.dict)
        final_data.code = 200
        final_data.data = "congratulation, you wrote a bill tip"
        final_data.time = get_end_back_time(bill_serializer.data["time"])
        final_data.money = bill_serializer.data["money"]
        final_data.remarks = bill_serializer.data["remarks"]
        return JsonResponse(final_data.dict, status=200)

    def get(self, request):
        """
        get list of bill tips
        :param request:
        :return:
        """
        final_data = BaseResponse()
        user_id = redis_obj.get("id")
        start_obj = request.data.get("start_time")
        end_obj = request.data.get("end_time")
        start_time = get_time_format(start_obj)
        end_time = get_time_format(end_obj)
        # get data what we want from database
        try:
            sum_query_set = BillDetail.objects.filter(user_id_id=user_id,
                                                      time__range=(start_time, end_time)).values("time", "money",
                                                                                                 "remarks",
                                                                                                 "user_id_id",
                                                                                                 "user_id__username"
                                                                                                 ).all()
            bill_ser = BillDetailSerializer(sum_query_set, many=True)
            final_data.data = bill_ser.data
            logger.info("bill-ser-data>>>>>", bill_ser.data)
        except Exception as e:
            logger.error(str(e))
            final_data.code = 300
            final_data.data = str(e) + "\n++database failed, try again"
            return JsonResponse(final_data.dict)
        finally_data_format = []
        out_dic = {}
        start_num = 0
        out_dic["full_data"] = []
        for query_object in sum_query_set:
            sum_money_dict = {}
            logger.info("query-object", query_object)
            sum_money_dict["username"] = query_object["user_id__username"]
            sum_money_dict["time"] = get_end_back_time(query_object["time"])
            sum_money_dict["money"] = query_object["money"]
            sum_money_dict["remarks"] = query_object["remarks"]
            start_num += query_object["money"]
            finally_data_format.append(sum_money_dict)
            out_dic["full_data"].append(sum_money_dict)
            out_dic["user_id"] = query_object["user_id_id"]
        # integrate data format
        final_data.code = 201
        final_data.msg = "you got what you want"
        final_data.data = out_dic
        final_data.total_money = start_num
        return JsonResponse(final_data.dict)


class LogoutApiView(APIView):
    def delete(self, request):
        """
        there is a bug, when you logout, you still could get all data, that couldn't happen any more
        :param request:
        :return:
        """
        final_obj = BaseResponse()
        request.session.delete("id")
        request.session.delete("TokenStr")
        redis_obj.delete("id")
        redis_obj.delete("TokenStr")
        id = redis_obj.get("id")
        logger.info("id from redis>>>", id)
        final_obj.code = 666
        final_obj.data = "you are out"
        logger.info(final_obj.dict)
        return JsonResponse(final_obj.dict)
