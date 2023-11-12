from django.contrib import admin
from .models import (citrix_log,
                     pre_process_date_usage_amount_data,
                     pre_process_online_amount_data,
                     application_authorizations_num,
                     airbox_data,
                     vanse_data)

admin.site.register(citrix_log)
admin.site.register(pre_process_date_usage_amount_data)
admin.site.register(pre_process_online_amount_data)
admin.site.register(application_authorizations_num)
admin.site.register(airbox_data)
admin.site.register(vanse_data)