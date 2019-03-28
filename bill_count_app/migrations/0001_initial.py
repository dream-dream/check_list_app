
# Generated by Django 2.1.7 on 2019-03-28 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.FloatField(verbose_name='time_for_now')),
                ('money', models.FloatField(verbose_name='money')),
                ('remarks', models.CharField(max_length=200, verbose_name='remarks')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='username')),
                ('phone_num', models.CharField(max_length=32, unique=True, verbose_name='telephone')),
                ('pwd', models.CharField(max_length=32, verbose_name='password')),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField(choices=[(0, 'female'), (1, 'male')], verbose_name='gender')),
                ('age', models.CharField(max_length=10)),
                ('job', models.CharField(max_length=32)),
                ('salary', models.IntegerField(choices=[(0, '<2000'), (1, '2000-5000'), (2, '5000-8000'), (3, '8000-10000'), (4, '10000<')], verbose_name='level_salary')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bill_count_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='billdetail',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bill_count_app.User'),
        ),
    ]
