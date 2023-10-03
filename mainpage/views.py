from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
from django.http import HttpResponseRedirect

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

    open_end_time['application_start_date'] = pd.to_datetime(open_end_time['application_start_date'], format="%m %d %Y, %H:%M:%S")
    open_end_time['application_end_date'] = pd.to_datetime(open_end_time['application_end_date'], format="%m %d %Y, %H:%M:%S")

    open_end_time['date'] = open_end_time['application_start_date'].dt.date
    open_end_time_grouped = open_end_time.groupby('date')

    max_concurrent_users = []

    for date, group in open_end_time_grouped:
        # 創建一個時間範圍，包含當天的所有時間點
        time_range = pd.date_range(start=date, end=date + pd.DateOffset(days=1), freq='T')

        # 初始化當天每個時間點的人數為0
        concurrent_users = [0] * len(time_range)

        # 對每一行資料，更新相應時間點的人數
        for _, row in group.iterrows():
            start_idx = (row['application_start_date'].datetime() - date).seconds // 60
            end_idx = (row['application_end_date'].datetime() - date).seconds // 60
            concurrent_users[start_idx:end_idx] += 1

        # 計算當天最高同時在線人數
        max_concurrent = max(concurrent_users)
        max_concurrent_users.append({'date': date, 'max_people': max_concurrent})

    result_df = pd.DataFrame(max_concurrent_users)
    result_df = result_df.sort_values(by='date')

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=result_df['date'],
                y=result_df['max_people'],
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
