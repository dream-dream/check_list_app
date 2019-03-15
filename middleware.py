from django.utils.deprecation import MiddlewareMixin


class MiddleCors(MiddlewareMixin):
    def process_request(self, request):
        print("i have already done")

    def process_response(self, request, response):
        print("that is not that difficult")
        response["Access-Control-Allow-Origin"] = ["*", ]
        return response
