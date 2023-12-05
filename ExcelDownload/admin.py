from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student

@admin.register(Student)
class PersonAdmin(ImportExportModelAdmin):
 list_display = ('id', 'schoolClass', 'className', 'schoolClassChinese', 'seatNumber', 'studentID', 'name', 'identityCard', 'sex', 'birth_date')