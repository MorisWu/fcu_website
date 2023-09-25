from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd

def mainpage(request):
    raw_data = citrix_log.objects.all()
    pd_data = pd.DataFrame(list(raw_data.values()))

    location_group = pd_data.groupby('location_name')
    application_group = location_group.get_group('3ds Max 2022')

    grouped = application_group.groupby(pd.Grouper(key='application_start_date', freq='D'))

    key_list = []
    num_list = []
    for i in grouped.groups.keys():
        key_list.append(i)

    for i in grouped.size():
        num_list.append(i)

    data_list = zip(key_list, num_list)

    return render(request,
                  'mainpage/index.html',
                  {
                    'data_list':data_list
                  })
