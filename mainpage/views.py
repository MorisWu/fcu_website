from django.shortcuts import render
from database_model.models import citrix_log

def mainpage(request):
    data_list = list(citrix_log.object.all())
    return render(request, 'mainpage/index.html', {'data_list':data_list})
