from django.shortcuts import render
from database_model.models import citrix_log
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
from django.http import HttpResponseRedirect

application_list = [
    '3ds Max 2022',
    'ACP 2022 R2',
    'Additive 2022 R2',
    'Aqwa 2022 R2',
    'AqwaWave 2022 R2',
    'ArcGlobe 101',
    'ArcMap 101',
    'ArcScene 101',
    'Archicad 26',
    'AutoCAD 2022',
    'AutoCAD 2023',
    'CFD-Post 2021 R2',
    'CFD-Post 2022 R2',
    'CFX 2021 R2',
    'CFX 2022 R2',
    'Cloudapp Online Usage',
    'ETABS 2015',
    'Ecotect Analysis 2011',
    'FlexSim 2020',
    'FlexSim 2022',
    'FlexSim 2023',
    'Fluent 2021 R2',
    'Fluent 2022 R2',
    'Iexplore',
    'Inventor 2022',
    'Inventor Professional 2023',
    'LS-Run 2022 R2',
    'LabVIEW 2021 SP1',
    'MATLAB R2022b',
    'Mechanical 2022 R2',
    'Mechanical APDL 2022 R2',
    'NI Multisim 141',
    'NX 85',
    'Navisworks Manage 2022',
    'Polarizer Surface Editor 2022 R2',
    'Polyflow 2022 R2',
    'Product & CAD Configuration 2022 R2',
    'RSM Job Monitoring 2022 R2',
    'Revit 2022',
    'Revit 2023',
    'Rhino 7',
    'SAP2000',
    'SOLIDWORKS 2016',
    'Sherlock 3D Viewer 2022 R2',
    'SpaceClaim 2022 R2',
    'Statistics on Structures 2022 R2',
    'VDI Online Usage',
    'Workbench 2021 R2',
    'Workbench 2022 R2',
    '校務系統',
    '校務系統練習區',
    '櫃台服務系統',
    '＊雲端校務123上課講義＊'
]

def mainpage(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        return render(request,'mainpage/index.html')

def citrix_log_open(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    location_group = citrix_log.objects.filter(location_name=app)
    pd_data = pd.DataFrame(list(location_group.values()))

    try:
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
                    name="test",
                    x=key_list,
                    y=num_list,
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

        context = {'data_list': data_list,
                   'bar': bar_div,
                   'app_name': [app],
                   'app_list': application_list}

        return render(request, 'citrix_log_page/open_amount.html', context)

    except:
        key_list = []
        num_list = []

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
                yaxis_title="number",
                xaxis_title="date",
                width=1500,
                height=750
            )
        )

        bar_div = opy.plot(trace, auto_open=False, output_type='div')

        context = {'data_list': data_list,
                   'bar': bar_div,
                   'app_name': [app],
                   'app_list': application_list}

        return render(request, 'citrix_log_page/open_amount.html', context)

def citrix_log_online(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    location_group = citrix_log.objects.filter(location_name=app)
    pd_data = pd.DataFrame(list(location_group.values()))

    try:
        open_end_time = pd_data[['application_start_date', 'application_end_date']]

        open_end_time['application_start_date'] = open_end_time['application_start_date']
        open_end_time['application_end_date'] = open_end_time['application_end_date']

        open_end_time['date'] = open_end_time['application_start_date'].dt.date
        open_end_time_grouped = open_end_time.groupby('date')

        max_online = open_end_time_grouped.apply(
            lambda x: x.apply(lambda y: ((x['application_start_date'] <= y['application_start_date']) & (
                        x['application_end_date'] >= y['application_end_date'])).sum(),
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
                   'app_name': [app],
                   'app_list': application_list}

        return render(request, 'citrix_log_page/online_amount.html', context)
    except:
        trace = go.Figure(
            data=[
                go.Bar(
                    name="test",
                    x=[],
                    y=[],
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
                   'app_name': [app],
                   'app_list': application_list}

        return render(request, 'citrix_log_page/online_amount.html', context)


