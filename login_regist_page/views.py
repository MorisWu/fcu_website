from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/mainpage/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/mainpage/')
    else:
        return render(request, 'login_regist_page/index.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('login/')

def regist(request):
    return render(request, 'login_regist_page/index.html')