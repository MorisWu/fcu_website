from django.shortcuts import render
from database_model.models import pre_process_online_amount_data, application_authorizations_num, vanse_data, airbox_data
import plotly.offline as opy
import plotly.graph_objs as go
from django.http import HttpResponseRedirect
from django.db.models import Max
import requests as res
import ast
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

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

    application_online_data = pre_process_online_amount_data.objects.filter(application_name=app).values('date__month').annotate(max_usage=Max('amount'))
    date_list = []
    num_list = []

    for i in application_online_data:
        date_list.append(i['date__month'])
        num_list.append(i['max_usage'])

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=date_list,
                y=num_list,
                offsetgroup=0,
                width=0.1
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title="number",
            xaxis_title="month",
            width=1500,
            height=750,
            xaxis=dict(
                tickmode='linear',
                dtick=1
            )
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

def vanse_month_data(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    application_usage_data = vanse_data.objects.filter(application_name=app).values('date__month').annotate(max_usage=Max('amount'))

    date_list = []
    num_list = []

    for i in application_usage_data:
        date_list.append(i['date__month'])
        num_list.append(i['max_usage'])

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=date_list,
                y=num_list,
                offsetgroup=0,
                width=0.1
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title="number",
            xaxis_title="month",
            width=1500,
            height=750,
            xaxis=dict(
                tickmode='linear',
                dtick=1
            )
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

    return render(request, 'citrix_log_page/vans_online_month_amount.html', context)

def citrix_vans_month_online(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    global application_list

    app = '校務系統'

    if 'application' in request.POST and request.POST['application'] != '':
        app = request.POST['application']

    application_online_data = pre_process_online_amount_data.objects.filter(application_name=app).values('date__month').annotate(max_usage=Max('amount')).order_by('date__month')
    vans_online_data = vanse_data.objects.filter(application_name=app).values('date__month').annotate(max_usage=Max('amount')).order_by('date__month')

    date_list = []
    num_list = []

    for i in application_online_data:
        date_list.append(i['date__month'])
        num_list.append(i['max_usage'])

    for i in vans_online_data:
        for j in range(len(date_list)):
            if i['date__month'] == date_list[j]:
                num_list[j] += i['max_usage']

    trace = go.Figure(
        data=[
            go.Bar(
                name="test",
                x=date_list,
                y=num_list,
                offsetgroup=0,
                width=0.1
            ),
        ],
        layout=go.Layout(
            title=app,
            yaxis_title="number",
            xaxis_title="month",
            width=1500,
            height=750,
            xaxis=dict(
                tickmode='linear',
                dtick=1
            )
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

def air_box(request):
    url = 'https://airbox.edimaxcloud.com/api/tk/query_now?token=ac59b57b-81fb-4fe2-a2e2-d49b25c7f8e5'
    get_raw_data = res.get(url).text
    data_dict = ast.literal_eval(get_raw_data)
    place_data_dict = {}
    offline_place_data_dict = {}

    if data_dict['status'] == 'ok':
        for data in data_dict['entries']:
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
        for data in data_dict['exclusion']:
            place_dict = {}
            place_dict['status'] = data['status']
            place_dict['time'] = data['time']
            offline_place_data_dict[data['name']] = place_dict

    context = {
        'place_data_dict':place_data_dict,
        'place_data_dict':place_data_dict,
        'offline_place_data_dict':offline_place_data_dict
    }
    return render(request, 'air_box/index.html', context)

'''
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
@register_job(scheduler,"interval", seconds=60, id='auto_add_data_in_to_air_box_database')
def auto_add_data_in_to_air_box_database():
    url = 'https://airbox.edimaxcloud.com/api/tk/query_now?token=ac59b57b-81fb-4fe2-a2e2-d49b25c7f8e5'
    get_raw_data = res.get(url).text
    data_dict = ast.literal_eval(get_raw_data)

    if data_dict['status'] == 'ok':
        for data in data_dict['entries']:
            airbox_data.objects.create(location = data['name'],
                                       pm25 = data['pm25'],
                                       pm10 = data['pm10'],
                                       pm1 = data['pm1'],
                                       co2 = data['co2'],
                                       hcho = data['hcho'],
                                       tvoc = data['tvoc'],
                                       co = data['co'],
                                       temperature = data['t'],
                                       humidity = data['h'],
                                       time = data['time']
                                       )

# 调度器开始运行
scheduler.start()
'''