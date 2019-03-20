from django.shortcuts import render


# Create your views here.
def register(request):
    return render(request, "register.html")


def login(request):
    return render(request, "login.html")


def input(request):
    return render(request, "input.html")


def get_list(request):
    return render(request, "get_list.html")


def get_detail(request):
    return render(request, "get_detail.html")
