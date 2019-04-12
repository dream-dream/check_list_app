import re
import logging
from rest_framework import serializers
from bill_count_app.models import User, UserDetail, BillDetail

logging = logging.getLogger("__name__")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'pwd', 'phone_num')

    def validate_username(self, attrs):
        if User.objects.filter(username=attrs).exists():
            raise serializers.ValidationError("the username already exist, could you try another one?")
        if len(attrs) < 5 or len(attrs) > 15:
            raise serializers.ValidationError("the username at least got 5 bits,at most got 15 bits")
        return attrs

    def validate_pwd(self, attrs):
        pwd_li = re.findall('^[a-zA-Z]\w{5,14}$', attrs)
        pwd = pwd_li[0]
        if not pwd and "":
            raise serializers.ValidationError(
                "the format was wrong，start with a letter，cantainer，at least 6 bits,at most 15 bits")
        return pwd

    def validate_phone_num(self, attrs):
        if attrs.isdigit():
            phone_num_li = re.findall('^1[345789]\d{9}$', attrs)
            if len(phone_num_li) is 0:
                raise serializers.ValidationError("phone number was wrong, try again")
            phone_num = phone_num_li[0]
            if not phone_num:
                raise serializers.ValidationError("the telephone number was wrong, could you try again")
            elif not phone_num.isdigit() and "":
                raise serializers.ValidationError("the format of telephone number must be all digits,come on!")
            return phone_num
        else:
            raise serializers.ValidationError("the format of telephone number must be all digits")

    def validate(self, attrs):
        pwd = attrs.get("pwd")
        username = attrs.get("username")
        phone_num = attrs.get("phone_num")
        if username is "" or phone_num is "" or pwd is "":
            raise serializers.ValidationError("sorry, username and telephone and password are required")
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ["gender", "age", "job", "salary", ]


class BillInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetail
        fields = ["time", "money", "remarks", "user_id_id"]


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=False)
    # pwd = serializers.CharField(required=False)
    # phone_num = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "pwd", "phone_num")


class BillDetailSerializer(serializers.ModelSerializer):
    # username = serializers.RelatedField(many=True, read_only=True)
    # user_id = serializers.RelatedField(many=True, read_only=True)
    # username = serializers.RegisterSerializer(
    #     many=True,
    #     read_only=True,
    # view_name='user_id_id',
    # )  # foreignkey field use argument--->source
    # user = RegisterSerializer()
    user = serializers.CharField(source="user_id__username")

    class Meta:
        model = BillDetail
        fields = ["time", "money", "remarks", "user_id_id", "user"]
        # fields = "__all__"
