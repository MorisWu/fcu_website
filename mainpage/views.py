from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd

def mainpage(request):
    raw_data = citrix_log.objects.all()
    pd_data = pd.DataFrame(list(raw_data.values()))

    location_group = pd_data.groupby('location_name').groups


    return render(request,
                  'mainpage/index.html',
                  {'data_list':location_group.keys()})
