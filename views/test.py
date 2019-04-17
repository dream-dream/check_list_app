"""
first i get frame,
second i get database,
finally get views, redis
"""
import time

print(time.time(), time.localtime())
import redis
# redis_obj = redis.Redis(host='localhost', port=6379, decode_responses=True)
# redis_obj.set('uuid', '5cad5ce2dc46d03aced294be')
# str_obj = redis_obj.get('uuid')
# print(str_obj, type(str_obj))
from flask import Flask
from flask import Blueprint, jsonify
from flask.views import MethodView

# the all-important app variable:
app = Flask(__name__)
api = Blueprint('api', __name__)


# @api.route("/hello/")
class Hello(MethodView):
    def get(self):
        dic = {}
        dic['msg'] = "hello world"
        return jsonify(dic)


# api.add_url_rule('/hello', 'hello', hello)
api.add_url_rule('/hello',
                 view_func=Hello.as_view("hello"))  # 404 page not found
if __name__ == "__main__":
    app.register_blueprint(api, url_prefix='/api/v1')
    app.run(host='127.0.0.1', debug=True, port=5000)
