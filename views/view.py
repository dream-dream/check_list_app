import re
import redis
import time
import random
import logging
from flask.views import MethodView
from flask import redirect, jsonify, request, Blueprint
from mongoengine.queryset.visitor import Q

from flask_check_list.views.models import User, UserDetail, BillDetail, \
    Token
from flask_check_list.response_code import BaseResponse
from flask_check_list.views.utils import get_str_time, get_time_format, \
    get_username, CheckLogin, get_gender, get_salary

# Create your views here.
# put login user id in redis
redis_con = redis.ConnectionPool(host="127.0.0.1", port=6379)
redis_obj = redis.Redis(connection_pool=redis_con)
api = Blueprint('api', __name__)


class Login(MethodView):
    def post(self):
        """
        login
        :param request:
        :return:
        """
        final_data = BaseResponse()
        request_json = request.json
        try:
            username = request_json['username']
            password = request_json['pwd']
        except Exception as e:
            final_data.code = 400
            final_data.data = str(e) + "/n input args was wrong, try again"
            return jsonify(final_data.dict)
        user_object = User.objects.get(username=username, pwd=password)
        if user_object:
            # set login status into session,
            # for the other interface check is login or not
            random_char = random.choice(
                [chr(random.randint(65, 90)), chr(random.randint(97, 122))])
            start_str = ""
            for i in range(5):
                provisional_str = str(random.randrange(10, 100)) + random_char
                start_str += provisional_str
            user_id = str(user_object.id)
            token = time.asctime() + start_str
            try:
                user_token = Token(token=user_id)
                user_token.save()
            except Exception as e:
                final_data.code = 300
                final_data.data = str(e) + "database failed，try again"
                return jsonify(final_data.dict)
            final_data.code = 200
            final_data.data = "you are in"
            final_data.username = username
            final_data.password = password
            final_data.token = token
            return jsonify(final_data.dict)
        else:
            final_data.code = 500
            final_data.data = "sorry, login failed, username or password " \
                              "was wrong, please try again"
            # logger.error(final_data)
            return jsonify(final_data.dict)


class Register(MethodView):
    def post(self):
        """
        register
        :param request:
        :return:
        """
        request_json = request.json
        final_data = BaseResponse()
        try:
            username = request_json["username"]
            phone_num = request_json["phone_num"]
            pwd = request_json["pwd"]
            re_pwd = request_json["re_pwd"]
            gender = request_json["gender"]
            age = request_json["age"]
            job = request_json["job"]
            salary = request_json["salary"]
        except Exception as e:
            final_data.code = 400
            final_data.data = str(e) + "/n input args was wrong, try again"
            return jsonify(final_data.dict)
        # todo checkout these fields
        if username is "" or phone_num is "" or pwd is "":
            final_data.code = 400
            final_data.data = "sorry, username and telephone and password " \
                              "are required"
            return jsonify(final_data.dict)

        is_username = User.objects(username=username)

        if is_username:
            final_data.code = 400
            final_data.data = "the username already exist, could you try " \
                              "another one?"
            return jsonify(final_data.dict)
        if username is not "" and (len(username) < 5 or len(username) > 15):
            final_data.code = 400
            final_data.data = "the username at least got 5 bits,at most got " \
                              "15 bits"
            return jsonify(final_data.dict)
        # todo use re model to checkout the telephone field
        if phone_num.isdigit():
            phone_num_li = re.findall('^1[345789]\d{9}$', phone_num)
            phone_num = phone_num_li[0]
            if not phone_num:
                final_data.code = 400
                final_data.data = "the telephone number was wrong, could you " \
                                  "try again"
                return jsonify(final_data.dict)
        elif not phone_num.isdigit() and "":
            final_data.code = 400
            final_data.data = "the format of telephone number must be all " \
                              "digits,come on!"
            return jsonify(final_data.dict)
        # todo checkout the power of pwd, got digit & character & symbol
        if pwd != re_pwd:
            final_data.code = 400
            final_data.data = "two passwords inconsistent，try again"
            return jsonify(final_data.dict)
        pwd_li = re.findall('^[a-zA-Z]\w{5,14}$', pwd)
        pwd = pwd_li[0]
        if not pwd and "":
            final_data.code = 400
            final_data.data = \
                "the format was wrong，start with a letter，cantainer，at " \
                "least 6 bits,at most 15 bits"
            return jsonify(final_data.dict)
        if pwd != re_pwd:
            final_data.code = 400
            final_data.data = "two passwords was different, try again"
            return jsonify(final_data.dict)
            # logger.info(user_ser.data, user_detail_ser.data)
        try:
            # to do rollback
            user_object = User(username=username,
                               phone_num=phone_num, pwd=pwd)
            # logger.debug("user_object", user_object)
            user_object.save()
            user_detail = UserDetail(user_id=user_object.id,
                                     gender=gender,
                                     age=age,
                                     job=job,
                                     salary=salary)
            user_detail.save()
        except Exception as e:
            final_data.code = 300
            final_data.data = str(e) + "/n database failed, try again"
            return jsonify(final_data.dict)
        final_data.code = 200
        final_data.data = 'congratulations register successful'
        final_data.username = user_object.username
        final_data.tele = user_object.phone_num
        final_data.gender = get_gender(user_detail.gender)
        final_data.age = user_detail.age
        final_data.job = user_detail.job
        final_data.salary = get_salary(user_detail.salary)
        return jsonify(final_data.dict)


class Bill(CheckLogin):
    def post(self):
        """
        submit bill tips
        :param request:
        :return:
        """
        final_data = BaseResponse()
        request_json = request.json
        try:
            money = request_json["money"]
            remarks = request_json["remarks"]
        except Exception as e:
            final_data.code = 400
            final_data.data = str(e) + "/n input args was wrong, try again"
            return jsonify(final_data.dict)
        this_moment = time.time()
        user_id = super(Bill, self).get()
        # logger.info("serializer", bill_serializer)
        try:
            bill_obj = BillDetail(time=this_moment, money=money,
                                  remarks=remarks,
                                  user=user_id)
            bill_obj.save()
        except Exception as e:
            final_data.code = 300
            final_data.data = str(e) + "database failed，try again"
            # logger.error(bill_serializer.errors, final_data.dict)
            return jsonify(final_data.dict)
        final_data.code = 200
        final_data.data = "congratulation, you wrote a bill tip"
        final_data.user = get_username(user_id)
        final_data.time = get_str_time(this_moment)
        final_data.money = money
        final_data.remarks = remarks
        return jsonify(final_data.dict)

    def get(self):
        """
        get list of bill tips
        :param request:
        :return:
        """
        final_data = BaseResponse()
        user_id = super(Bill, self).get()
        request_json = request.json
        try:
            start_obj = request_json["start_time"]
            end_obj = request_json["end_time"]
        except Exception as e:
            final_data.code = 400
            final_data.data = str(e) + "/n input args was wrong, try again"
            return jsonify(final_data.dict)
        start_time = get_time_format(start_obj)
        end_time = get_time_format(end_obj)
        # get data what we want from database
        try:
            sum_query_set = BillDetail.objects(
                Q(time__lte=end_time) & Q(time__gte=start_time) & Q(
                    user=user_id)).all()
            # logger.info("bill-ser-data>>>>>", bill_ser.data)
        except Exception as e:
            # logger.error(str(e))
            final_data.code = 300
            final_data.data = str(e) + "\n++database failed, try again"
            return jsonify(final_data.dict)
        start_num = 0
        final_data.data = []
        for query_object in sum_query_set:
            print("query-object", query_object.user, query_object.time,
                  query_object.money, query_object.remarks)
            sum_money_dict = {}
            # logger.info("query-object", query_object)
            sum_money_dict["time"] = get_str_time((query_object.time))
            sum_money_dict["money"] = query_object.money
            sum_money_dict["remarks"] = query_object.remarks
            start_num += query_object.money
            final_data.data.append(sum_money_dict)
        # integrate data format
        final_data.code = 201
        final_data.msg = "you got what you want"
        final_data.username = get_username(user_id)
        final_data.total_money = start_num
        return jsonify(final_data.dict)


class BillList(MethodView):
    def get(self):
        finally_data = BaseResponse()
        try:
            bill_obj = BillDetail.objects().all()
            sum_money = BillDetail.objects().sum('money')
        except Exception as e:
            finally_data.code = 300
            finally_data.error = str(e) + "\n++database failed, try again"
            return jsonify(finally_data.dict)
        finally_data.data = []
        for query in bill_obj:
            fina_dic = {}
            fina_dic['user'] = get_username(query.user)
            fina_dic['time'] = query.time
            fina_dic['remarks'] = query.remarks
            fina_dic['money'] = query.money
            finally_data.data.append(fina_dic)
        finally_data.code = 201
        finally_data.msg = "you got what you want"
        finally_data.totale = sum_money
        return jsonify(finally_data.dict)


class Logout(CheckLogin):
    def delete(self):
        """
        there is a bug, when you logout, you still could get all data, that couldn't happen any more
        :param request:
        :return:
        """
        final_obj = BaseResponse()
        try:
            super(Logout, self).get()
            token_obj = Token.objects().first()
            token_obj.delete()
        except Exception as e:
            final_obj.code = 300
            final_obj.error = str(e) + "\n++database failed, try again"
            return jsonify(final_obj.dict)
        # logger.info("id from redis>>>", id)
        final_obj.code = 666
        final_obj.data = "you are out"
        # logger.info(final_obj.dict)
        return jsonify(final_obj.dict)


api.add_url_rule('/login', view_func=Login.as_view('login'))
api.add_url_rule('/register', view_func=Register.as_view('register'))
api.add_url_rule('/bill', view_func=Bill.as_view('bill'))
api.add_url_rule('/bill_list', view_func=BillList.as_view('bill_list'))
api.add_url_rule('/logout', view_func=Logout.as_view('logout'))