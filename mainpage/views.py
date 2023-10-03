from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
from django.http import HttpResponseRedirect
import pytz

def mainpage(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        return render(request,'mainpage/index.html')

def citrix_log_open(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    location_group = citrix_log.objects.filter(location_name=app)
    pd_data = pd.DataFrame(list(location_group.values()))

    grouped = pd_data.groupby(pd.Grouper(key='application_start_date', freq='D'))

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
                name = "test",
                x=key_list,
                y=num_list,
                offsetgroup=0,
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title = "number",
            xaxis_title = "date",
            width = 1500,
            height = 750
        )
    )

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    context = {'data_list':data_list,
               'bar':bar_div,
               'app_name':[app]}

    return render(request,'citrix_log_page/open_amount.html', context)

def citrix_log_online(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    location_group = citrix_log.objects.filter(location_name=app)
    pd_data = pd.DataFrame(list(location_group.values()))

    open_end_time = pd_data[['application_start_date', 'application_end_date']]

    open_end_time['application_start_date'] = open_end_time['application_start_date']
    open_end_time['application_end_date'] = open_end_time['application_end_date']

    open_end_time['date'] = open_end_time['application_start_date'].dt.date
    open_end_time_grouped = open_end_time.groupby('date')

    max_online = open_end_time_grouped.apply(
        lambda x: x.apply(lambda y: ((x['application_start_date'] <= y['application_start_date']) & (x['application_end_date'] >= y['application_end_date'])).sum(),
                          axis=1).max())

    result_df = pd.DataFrame({'date': max_online.index, 'max_amount': max_online.values})
    result_df = result_df.sort_values(by='date')

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=result_df['date'],
                y=result_df['max_amount'],
                offsetgroup=0,
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title="number",
            xaxis_title="date",
            width=1500,
            height=750
        )
    )

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    context = {'bar': bar_div,
               'app_name': [app]}

    return render(request, 'citrix_log_page/open_amount.html', context)
