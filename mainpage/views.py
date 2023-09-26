from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
from django.http import HttpResponseRedirect

def mainpage(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    location_group = citrix_log.objects.filter(location_name=app)
    pd_data = pd.DataFrame(list(location_group.values()))

    grouped = pd_data.groupby(pd.Grouper(key='application_start_date', freq='H'))

    key_list = []
    num_list = []
    for i in grouped.groups.keys():
        key_list.append(i)

    for i in grouped.size():
        num_list.append(i)

    data_list = zip(key_list, num_list)

    # 每次显示的数据点数量
    data_points_per_slice = 4

    # 初始显示的数据切片
    start_index = 0
    end_index = start_index + data_points_per_slice

    trace = go.Figure(
        data=[
            go.Bar(
                name = "test",
                x=key_list,
                y=num_list,
                offsetgroup=0,
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title = "num",
            xaxis_title = "date",
            xaxis=key_list[start_index, end_index],
            width = 1500,
            height = 750
        )
    )

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    context = {'data_list':data_list,
               'bar':bar_div,
               'app_name':[app]}

    return render(request,'mainpage/index.html', context)
