from django.shortcuts import render
from django.http import HttpResponse

def login_regist(request):
    return render(request, 'login_regist_page/index.html')
