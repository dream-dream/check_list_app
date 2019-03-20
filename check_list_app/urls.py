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
from fore_end import views as fore_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', views.login, name='api_login'),
    path('api/v1/logout/', views.logout, name='api_logout'),
    path('api/v1/register/', views.register, name='api_register'),
    path('api/v1/input/', views.input, name='api_input'),
    path('api/v1/get_list/', views.get_list, name='api_get_list'),
    path('api/v1/get_detail/', views.get_detail, name='api_get_detail'),
    path('login/', fore_view.login, name='login'),
    path('register/', fore_view.register, name='register'),
    path('input/', fore_view.input, name='input'),
    path('get_list/', fore_view.get_list, name='get_list'),
    path('get_detail/', fore_view.get_detail, name='get_detail'),

]

