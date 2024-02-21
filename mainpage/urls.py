from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage),

    path('citrix_online_monthly/', views.month_online),
    path('vanse_online_monthly/', views.vanse_month_data),
    path('vans_citrix_monthly/', views.citrix_vans_month_online),

    path('citrix_online_weekly/', views.citrix_week_online),

    path('air_box/', views.air_box),
    path('air_box_graph/', views.air_box_garph)
]
