from django.shortcuts import render
import requests as res
import ast
from models import airbox_data

def auto_add_data_in_to_air_box_database():
    url = 'https://airbox.edimaxcloud.com/api/tk/query_now?token=ac59b57b-81fb-4fe2-a2e2-d49b25c7f8e5'
    get_raw_data = res.get(url).text
    data_dict = ast.literal_eval(get_raw_data)

    if data_dict['status'] == 'ok':
        for data in data_dict['entries']:
            airbox_data.objects.create(location=data['name'],
                                       pm25=data['pm25'],
                                       pm10=data['pm10'],
                                       pm1=data['pm1'],
                                       co2=data['co2'],
                                       hcho=data['hcho'],
                                       tvoc=data['tvoc'],
                                       co=data['co'],
                                       temperature=data['t'],
                                       humidity=data['h'],
                                       time=data['time']
                                       )