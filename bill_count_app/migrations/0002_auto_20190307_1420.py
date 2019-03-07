# Generated by Django 2.1.7 on 2019-03-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_count_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billdetail',
            name='time',
            field=models.DecimalField(decimal_places=100, max_digits=200, verbose_name='当前时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_num',
            field=models.CharField(max_length=32, unique=True, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=32, unique=True, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='salary',
            field=models.IntegerField(choices=[(0, '<2000'), (1, '2000-5000'), (2, '5000-8000'), (3, '8000-10000'), (4, '10000<')], verbose_name='薪水级别'),
        ),
    ]
