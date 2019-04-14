import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mongoengine import *
from .. import db
from mongoengine import ObjectIdField
# Create your models here.


class User(db.Document):
    meta = {
        'collection': 'user',
        'strict': False,
    }
    username = db.StringField(required=True, max_length=30, unique=True)
    phone_num = db.StringField(required=True, max_length=32, unique=True)
    pwd = db.StringField(required=True, max_length=32)

    # def __repr__(self):
    #     return self.username


class UserDetail(db.Document):
    meta = {
        'collection': 'userdetail',
        'strict': False,
    }
    user_id = ObjectIdField()
    gender_opt = ((0, 'female'), (1, 'male'))
    gender = db.IntField(choices=gender_opt)
    age = db.IntField(10)
    job = db.StringField(required=True, max_length=32)
    salary_opt = (
        (0, '<2000'),
        (1, '2000-5000'),
        (2, '5000-8000'),
        (3, '8000-10000'),
        (4, '10000<')
    )
    salary = db.IntField(choices=salary_opt)
    # meta = {"db_alias": 'test'}

    # @classmethod
    # def get_gender(self, arg):
    #     gender_opt = ['female', 'male']
    #     return gender_opt[arg]
    #
    # @classmethod
    # def get_salary(self, arg):
    #     salary_opt = ['<2000', '2000-5000', '5000-8000', '8000-10000', '10000<']
    #     return salary_opt[arg]

    # def __repr__(self):
    #     return self.job


class BillDetail(db.Document):
    meta = {
        'collection': 'billdetail',
        'strict': False,
    }
    user = ObjectIdField()
    time = db.FloatField()
    money = db.FloatField()
    remarks = db.StringField(required=True, max_length=200)

    # def __repr__(self):
    #     return self.remarks


class Token(db.Document):
    meta = {
        'collection': 'token',
        'strict': False,
    }
    token = db.ObjectIdField()



