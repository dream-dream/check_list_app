from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse
# from bill_count_app.models import User
import random
import time


class MiddleCors(MiddlewareMixin):
    def process_request(self, request):
        # print("hello world")
        pass

    def process_response(self, request, response):
        # if request.session.get("id") and request.session.get("TokenStr"):
        ret = HttpResponse(response)
        ret['Access-Control-Allow-Origin'] = '*'
        ret["Access-Control-Allow-Methods"] = "POST,GET,OPTION,PUT,DELETE,PATCH"
        return response
        # else:
        #     return redirect("login/")
