from django.urls import path
from . import views
app_name = "bill_count_app"
urlpatterns = [
    path("login/", views.LoginApiView.as_view()),
    path("register/", views.RegisterApiView.as_view()),
    path("bill/", views.BillApiView.as_view()),
]