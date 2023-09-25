from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd

def mainpage(request):
    raw_data = citrix_log.objects.all()
    pd_data = pd.DataFrame(list(raw_data.values()))
    time_data_list = []

    for i in pd_data['application_start_date']:
        time_data_list.append(i)

    return render(request,
                  'mainpage/index.html',
                  {'data_list':time_data_list})
