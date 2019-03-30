from rest_framework import serializers
from bill_count_app.models import User, UserDetail, BillDetail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'pwd', 'phone_num')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = "__all__"


class BillDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user_id_id.username")  # foreignkey field use argument--->source

    class Meta:
        model = BillDetail
        fields = ["time", "money", "remarks", "user_id_id", "username"]

