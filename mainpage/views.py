from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd

def mainpage(request):
    raw_data = citrix_log.objects.all()
    data_list = list(raw_data)
    t = list(type(raw_data))
    return render(request,
                  'mainpage/index.html',
                  {'data_list':data_list,
                   'type':t})
