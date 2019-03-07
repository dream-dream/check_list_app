from django.db import models

# Create your models here.


class User(models.Model):
    # user_id = models.IntegerField(verbose_name='用户ID', null=False)
    username = models.CharField(max_length=32, unique=True, null=False, blank=False, verbose_name='用户名')
    phone_num = models.CharField(max_length=32, unique=True, null=False, blank=False, verbose_name='手机号')
    pwd = models.CharField(max_length=32, null=False, blank=False, verbose_name='用户密码')

    def __str__(self):
        return self.username


class UserDetail(models.Model):
    gender_opt = ((0, 'female'), (1, 'male'))
    user_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    gender = models.IntegerField(choices=gender_opt, verbose_name='性别')
    age = models.CharField(max_length=10)
    job = models.CharField(max_length=32)
    salary_opt = ((0, '<2000'), (1, '2000-5000'), (2, '5000-8000'), (3, '8000-10000'), (4, '10000<'))
    salary = models.IntegerField(choices=salary_opt, verbose_name='薪水级别')

    def __str__(self):
        return self.job


class BillDetail(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    time = models.DecimalField(max_digits=200, decimal_places=100, verbose_name='当前时间')
    money = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='输入金额')
    remarks = models.CharField(max_length=200, verbose_name='备注信息')

    def __str__(self):
        return self.remarks




