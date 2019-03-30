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
from rest_framework import routers
from django.urls import path, include
from bill_count_app import views

from fore_end import views as fore_view
router = routers.DefaultRouter()
# router.register(r'register', views.register)  # register only for viewset
# router.register(r'login', views.login)
# router.register(r'user', views.UserViewSet)
# router.register(r'bill', views.BillApiView)
# router.register(r'user_detail', views.UserDetailViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include(router.urls)),  # for quick-start
    # path('api/v1/login/', views.LoginApiView.as_view()),
    # path('api/v1/logout/', views.logout),
    # path('api/v1/register/', views.register),
    # path('api/v1/input/', views.input),
    # path('api/v1/get_list/', views.get_list),
    # path('api/v1/get_detail/', views.get_detail),
    # path('login/', fore_view.login),
    # path('register/', fore_view.register),
    # path('input/', fore_view.input),
    # path('get_list/', fore_view.get_list),
    # path('get_detail/', fore_view.get_detail),
    path('api/v1/', include("bill_count_app.urls", namespace='bill_count_app')),

]

