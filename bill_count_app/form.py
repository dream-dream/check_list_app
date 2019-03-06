from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from bill_count_app.models import User, UserDetail, BillDetail


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=16, min_length=6, error_messages={"required": "不能为空",
                                                                            "max_length": "最大长度是16",
                                                                            "min_length": "最小长度是6"})
    mobile = forms.CharField(max_length=11, min_length=11, error_messages={"required": "不能为空",
                                                                           "max_length": "长度只能是11位"})
    password = forms.CharField(max_length=16, min_length=6, error_messages={"required": "不能为空",
                                                                            "max_length": "最大长度是16",
                                                                            "min_length": "最小长度是6"})
    re_pwd = forms.CharField(max_length=16, min_length=6, error_messages={"required": "不能为空",
                                                                          "max_length": "最大长度是16",
                                                                          "min_length": "最小长度是6"})
    gender = forms.ChoiceField(initial=0, widget=widgets.Select(choices=((0, '女'), (1, '男'))))
    age = forms.CharField(max_length=16, min_length=6, error_messages={"required": "不能为空",
                                                                       "max_length": "最大长度是16",
                                                                       "min_length": "最小长度是6"})
    job = forms.CharField(max_length=16, min_length=6, error_messages={"required": "不能为空",
                                                                       "max_length": "最大长度是16",
                                                                       "min_length": "最小长度是6"})
    salary = forms.IntegerField(max_value=50, min_value=10)

    def clean_mobile(self):
        phone_num = self.cleaned_data.get("mobile")
        is_phone = User.objects.filter(phone_num=phone_num).exists()
        import re
        re_search_num = re.findall('^1[345789]\d{9}$', phone_num)
        if is_phone:
            raise ValidationError("该手机号已经注册，请重试")
        elif not re_search_num:
            raise ValidationError("格式错误，请重试")
        else:
            return phone_num

    def clean_name(self):
        username = self.cleaned_data.get('username')
        is_name = User.objects.filter(username=username).exists()
        if is_name:
            raise ValidationError("该用户名已经注册，请重试")
        else:
            return username

    def clean(self):
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致，请重新输入")
