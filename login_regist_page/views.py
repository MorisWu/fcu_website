from django.shortcuts import render
from django.contrib import auth

def login_regist(request):
    return render(request, 'login_regist_page/index.html')

