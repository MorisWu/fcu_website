from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd

def mainpage(request):
    data_list = list(citrix_log.objects.all())

    pd_data = pd.DataFrame(data_list)
    pd_data['application_start_date'] = pd.to_datetime(pd_data['application_start_date'])

    return render(request, 'mainpage/index.html', {'data_list':data_list})
