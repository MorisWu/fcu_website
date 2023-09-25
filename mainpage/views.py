from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd

def mainpage(request):
    raw_data = citrix_log.objects.all()
    pd_data = pd.DataFrame(list(raw_data.values()))

    location_group = pd_data.groupby('location_name')
    application_group = location_group.get_group('3ds Max 2022')

    data_list = []

    grouped = application_group.groupby(pd.Grouper(key='application_start_date', freq='D'))

    for i, j in grouped.groups.keys(), grouped.size():
        data_list.append(str(i) + str(j))

    return render(request,
                  'mainpage/index.html',
                  {'data_list':data_list})
