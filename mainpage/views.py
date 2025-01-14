import datetime
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as opy
import requests as res
from django.db.models import Max
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from database_model.models import pre_process_online_amount_data, application_authorizations_num, vanse_data, \
    airbox_data

application_list = [
    '3ds Max 2022',
    'ACL 16',
    'ACP 2022 R2',
    'Access',
    'Additive 2022 R2',
    'Adobe Acrobat X Pro',
    'Aqwa 2022 R2',
    'AqwaWave 2022 R2',
    'ArcGlobe 101',
    'ArcMap 101',
    'ArcScene 101',
    'Archicad 26',
    'AutoCAD 2022',
    'AutoCAD 2023',
    'CFD-Post 2022 R2',
    'CFX 2022 R2',
    'Cloudapp Online Usage',
    'DESIGN II',
    'Design Point Service DPS 2022 R2',
    'ETABS 2015',
    'EViews 11',
    'Ecotect Analysis 2011',
    'Excel',
    'FlexSim 2020',
    'FlexSim 2022',
    'FlexSim 2023',
    'Fluent 2021 R2',
    'Fluent 2022 R2',
    'Iexplore',
    'Inkscape',
    'Inventor 2022',
    'Inventor Professional 2023',
    'Kdenlive',
    'Krita',
    'LS-Run 2022 R2',
    'LabVIEW 2021 SP1',
    'LabVIEW 2023',
    'LibreOffice',
    'LibreOffice Base',
    'LibreOffice Calc',
    'LibreOffice Draw',
    'LibreOffice Impress',
    'MATLAB R2022b',
    'MATLAB R2023a',
    'Mechanical 2022 R2',
    'Mechanical APDL 2022 R2',
    'Mechanical APDL Product Launcher 2022 R2',
    'Minitab',
    'NI Multisim 141',
    'NI Ultiboard 141',
    'NX 85',
    'Navisworks Manage 2022',
    'Polarizer Surface Editor 2022 R2',
    'Polyflow 2022 R2',
    'PowerPoint',
    'Product & CAD Configuration 2022 R2',
    'RSM Job Monitoring 2022 R2',
    'RStudio',
    'Revit 2022',
    'Revit 2023',
    'Rhino 7',
    'SAP2000',
    'SAS 94 中文',
    'SAS 94 英文',
    'SAS Enterprise Guide 83',
    'SAS Enterprise Miner Workstation 152',
    'SAS Studio 381',
    'SOLIDWORKS 2016',
    'SPSS 18',
    'SPSS 21',
    'SPSS 22',
    'SPSS 23',
    'SPSS 24',
    'Sherlock 2022 R2',
    'Sherlock 3D Viewer 2022 R2',
    'SmartPLS 4',
    'SpaceClaim 2022 R2',
    'StataSE 18',
    'Statistics on Structures 2022 R2',
    'TEJPro',
    'VDI Online Usage',
    'Visio',
    'Word',
    'WorkFlow ERP GP 系統',
    'Workbench 2021 R2',
    'Workbench 2022 R2',
    '幼獅題庫命題系統107年',
    '校務系統',
    '校務系統練習區',
    '櫃台服務系統',
    '＊雲端校務123上課講義＊'
]

location_list = [
    '人言_405',
    '人言_402',
    '人言_503',
    '人言_502',
    '人言_707',
    '人言_603',
    '人言_401',
    '人言_608',
    '人言_607',
    '資電_IDC機房',
    '人言_704',
    '人言_504',
    '人言_604',
    '人言_404',
    '人言_605',
    '人言_703',
    '人言_506',
    '人言_702',
    '人言_701',
    '人言_403',
    '人言_407',
    '人言_706',
    '人言_708',
    '人言_507',
    '人言_505',
    '人言_606',
    '人言_501',
    '人言_B120',
    '人言_508',
    '人言_202',
    '人言_203',
    '人言_B119',
    '人言_408',
    '人言_B117',
    '人言_B116',
    '人言_705',
    '資電_248',
    '紀念_303',
    '工學_319',
    '紀念_302',
    '資電_234',
]

air_data_list = [
    'pm25',
    'pm10',
    'co2',
    'hcho',
    'tvoc',
    'co'
]


def mainpage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'mainpage/index.html')


def month_online(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    application_online_data = pre_process_online_amount_data.objects.filter(application_name=app).annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(
        max_usage=Max('amount')
    ).order_by('year', 'month')

    date_list = []
    num_list = []

    for i in application_online_data:
        year_month = f"{i['year']}-{str(i['month']).zfill(2)}"  # 格式化為 'YYYY-MM'
        date_list.append(year_month)
        num_list.append(i['max_usage'])

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=date_list,
                y=num_list,
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title="number",
            xaxis_title="month",
            width=1500,
            height=750,
        )
    )

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    auth_num = 0
    try:
        auth = application_authorizations_num.objects.filter(application_name=app)
        for i in auth:
            auth_num = i.amount
    except:
        auth_num = 0

    context = {'bar': bar_div,
               'app_name': [app],
               'app_list': application_list,
               'auth_num': [auth_num]
               }

    return render(request, 'citrix_log_page/online_month_amount.html', context)


def citrix_week_online(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    pd_dataframe = pd.DataFrame.from_records(
        pre_process_online_amount_data.objects.filter(application_name=app).values())

    pd_dataframe = pd_dataframe.resample('w', on='date').max()

    trace = px.bar(pd_dataframe, x=pd_dataframe.index, y='amount', title=app)

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    context = {'bar': bar_div,
               'app_name': [app],
               'app_list': application_list,
               }

    return render(request, 'citrix_log_page/citrix_week_amount.html', context)


def vanse_month_data(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    application_usage_data = vanse_data.objects.filter(application_name=app).annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(
        max_usage=Max('amount')
    ).order_by('year', 'month')

    date_list = []
    num_list = []

    for i in application_usage_data:
        year_month = f"{i['year']}-{str(i['month']).zfill(2)}"  # 格式化為 'YYYY-MM'
        date_list.append(year_month)
        num_list.append(i['max_usage'])

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=date_list,
                y=num_list,
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title="number",
            xaxis_title="month",
            width=1500,
            height=750,
        )
    )

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    auth_num = 0
    try:
        auth = application_authorizations_num.objects.filter(application_name=app)
        for i in auth:
            auth_num = i.amount
    except:
        auth_num = 0

    context = {'bar': bar_div,
               'app_name': app,
               'app_list': application_list,
               'auth_num': [auth_num]
               }

    return render(request, 'citrix_log_page/vans_online_month_amount.html', context)


def vanse_week_data(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    pd_dataframe = pd.DataFrame.from_records(vanse_data.objects.filter(application_name=app).values())

    try:
        pd_dataframe = pd_dataframe.resample('w', on='date').max()
        trace = px.bar(pd_dataframe, x=pd_dataframe.index, y='amount', title=app)
    except:
        trace = px.bar(x=[datetime.date.today()], y=[0], title=app)

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    context = {'bar': bar_div,
               'app_name': [app],
               'app_list': application_list,
               }

    return render(request, 'citrix_log_page/vanse_week_amount.html', context)


def citrix_vans_month_online(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    application_online_data = pre_process_online_amount_data.objects.filter(application_name=app).annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(
        max_usage=Max('amount')
    ).order_by('year', 'month')

    vans_online_data = vanse_data.objects.filter(application_name=app).annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(
        max_usage=Max('amount')
    ).order_by('year', 'month')

    date_list = []
    num_list = []

    for i in application_online_data:
        year_month = f"{i['year']}-{str(i['month']).zfill(2)}"  # 格式化為 'YYYY-MM'
        date_list.append(year_month)
        num_list.append(i['max_usage'])

    for i in vans_online_data:
        year_month = f"{i['year']}-{str(i['month']).zfill(2)}"
        for j in range(len(date_list)):
            if year_month == date_list[j]:
                num_list[j] += i['max_usage']

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=date_list,
                y=num_list,
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title="number",
            xaxis_title="month",
            width=1500,
            height=750,
        )
    )

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    auth_num = 0
    try:
        auth = application_authorizations_num.objects.filter(application_name=app)
        for i in auth:
            auth_num = i.amount
    except:
        auth_num = 0

    context = {'bar': bar_div,
               'app_name': [app],
               'app_list': application_list,
               'auth_num': [auth_num]
               }

    return render(request, 'citrix_log_page/citrix_vans_month_amount.html', context)


def citrix_vanse_week_data(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    citrix_pd_dataframe = pd.DataFrame.from_records(
        pre_process_online_amount_data.objects.filter(application_name=app).values())

    vanse_pd_dataframe = pd.DataFrame.from_records(
        vanse_data.objects.filter(application_name=app).values())

    pd_dataframe = pd.concat([citrix_pd_dataframe, vanse_pd_dataframe])

    pd_dataframe = pd_dataframe.resample('w', on='date').max()

    trace = px.bar(pd_dataframe, x=pd_dataframe.index, y='amount', title=app)

    bar_div = opy.plot(trace, auto_open=False, output_type='div')

    context = {'bar': bar_div,
               'app_name': [app],
               'app_list': application_list,
               }

    return render(request, 'citrix_log_page/citrix_vanse_week_amount.html', context)


def air_box(request):
    url = 'https://airbox.edimaxcloud.com/api/tk/query_now?token=ac59b57b-81fb-4fe2-a2e2-d49b25c7f8e5'
    get_raw_data = res.get(url).text #取得json格式的data(文本型態)
    data_dict = json.loads(get_raw_data)#將data轉換為dict
    place_data_dict = {}
    offline_place_data_dict = {}

    '''
    閾值設定
    '''
    values_threshold = {
        'pm25': 35,
        'pm10': 75,
        'pm1': 35,
        'co2': 1000,
        'hcho': 0.08,
        'tvoc': 0.56,
        'co': 9
    }

    value_keys = values_threshold.keys() #取得所有資料的key

    if data_dict['status'] == 'ok':
        for data in data_dict['exclusion']: #在線機器資料
            place_dict = {}
            place_dict['pm25'] = data['pm25']
            place_dict['pm10'] = data['pm10']
            place_dict['pm1'] = data['pm1']
            place_dict['co2'] = data['co2']
            place_dict['hcho'] = data['hcho']
            place_dict['tvoc'] = data['tvoc']
            place_dict['co'] = data['co']
            place_dict['t'] = data['t']
            place_dict['h'] = data['h']
            place_dict['status'] = data['status']
            place_dict['time'] = data['time']
            place_data_dict[data['name']] = place_dict
            place_dict['color'] = "white"
            for key in value_keys:
                if place_dict[key] > values_threshold[key]: #若超出閾值則將格子背景設為紅色
                    place_dict['color'] = "red"
                    break
        for data in data_dict['exclusion']: #離線機器資料
            place_dict = {}
            place_dict['status'] = data['status']
            place_dict['time'] = data['time']
            offline_place_data_dict[data['name']] = place_dict

    values_threshold = {
        'pm25': 35,
        'pm10': 75,
        'pm1': 35,
        'co2': 1000,
        'hcho': 0.08,
        'tvoc': 0.56,
        'co': 9
    }

    context = {
        'place_data_dict': place_data_dict,
        'offline_place_data_dict': offline_place_data_dict,
        'values_threshold': values_threshold,
    }

    return render(request, 'air_box/index.html', context)


def air_box_garph(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global location_list, air_data_list

    location = location_list[0]
    air = air_data_list[0]

    if 'location' in request.POST and request.POST['location'] != '' and request.POST['air'] != '':
        location = request.POST['location']
        air = request.POST['air']

    air_data = airbox_data.objects.filter(location=location)

    data_list = []
    time_list = []

    for data in air_data.values():
        data_list.append(data[air])
        time_list.append(data['time'])

    if air == 'pm10' or air == 'pm25':
        data_dict = {
            'time': time_list,
            'μg/m': data_list,
        }

        air_trace = px.line(
            data_dict,
            x='time',
            y='μg/m',
            title=air,
        )
    else:
        data_dict = {
            'time': time_list,
            'ppm': data_list
        }

        air_trace = px.line(
            data_dict,
            x='time',
            y='ppm',
            title=air,
        )

    air_div = opy.plot(air_trace, auto_open=False, output_type='div')

    context = dict(air_graph=air_div,
                   location_list=location_list,
                   air_data_list=air_data_list,
                   location=location,
                   air=air)

    return render(request, 'air_box/air_box_graph.html', context)
