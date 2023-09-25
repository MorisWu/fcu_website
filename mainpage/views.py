from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd

def mainpage(request):
    raw_data = citrix_log.objects.all()
    data_list = list(raw_data)

    pd_data = pd.DataFrame(raw_data)
    pd_data['application_start_date'] = pd.to_datetime(pd_data['application_start_date'])

    return render(request, 'mainpage/index.html', {'data_list':data_list})
