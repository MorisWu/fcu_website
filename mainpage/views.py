from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
from django.http import HttpResponseRedirect

def mainpage(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    raw_data = citrix_log.objects.all()
    pd_data = pd.DataFrame(list(raw_data.values()))

    location_group = pd_data.groupby('location_name')
    app = '校務系統'
    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']


    application_group = location_group.get_group(app)

    grouped = application_group.groupby(pd.Grouper(key='application_start_date', freq='D'))

    key_list = []
    num_list = []
    for i in grouped.groups.keys():
        key_list.append(i)

    for i in grouped.size():
        num_list.append(i)

    data_list = zip(key_list, num_list)

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=key_list,
                y=num_list,
                offsetgroup=0,
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title="num",
            xaxis_title = "date"
        )
    )

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    context = {'data_list':data_list,
               'bar':bar_div,
               'app_name':[app]}

    return render(request,'mainpage/index.html', context)
