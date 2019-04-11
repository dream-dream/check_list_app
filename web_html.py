# coding=utf-8
from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

# 创建静态文件蓝图
html = Blueprint("html", __name__)


# 创建静文件路由
@html.route('/<re(".*"):filename>')
def get_html(filename):
    # 如果是首页则没有filename参数 直接跳转到index
    if not filename:
        filename = '/index.html'

    print(filename)
    # 生成 csrf_token
    csrf_token = generate_csrf()
    response = make_response(current_app.send_static_file(filename))
    response.set_cookie("csrf_token", csrf_token)
    return response
