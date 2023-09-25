from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd

def mainpage(request):
    raw_data = citrix_log.objects.all()
    data_list = list(raw_data)
    data_type = str(type(raw_data))
    df = pd.DataFrame(list(raw_data.values()))

    return render(request,
                  'mainpage/index.html',
                  {'data_list':data_list,
                   'type_list':[data_type]})
