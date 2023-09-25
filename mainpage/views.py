from django.shortcuts import render
from database_model.models import citrix_log

def mainpage(request):
    data_list = list(citrix_log.user_name.all())
    return render(request, 'mainpage/index.html', locals())