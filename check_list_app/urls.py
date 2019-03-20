"""check_list_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bill_count_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', views.login, name='api_login'),
    path('api/v1/logout/', views.logout, name='api_logout'),
    path('api/v1/register/', views.register, name='api_register'),
    path('api/v1/input/', views.input, name='api_input'),
    path('api/v1/get_list/', views.get_list, name='api_get_list'),
    path('api/v1/get_detail/', views.get_detail, name='api_get_detail'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('input/', views.input, name='input'),
    path('get_list/', views.get_list, name='get_list'),
    path('get_detail/', views.get_detail, name='get_detail'),

]
