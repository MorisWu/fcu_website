from django.db import models

# Create your models here.
class Student(models.Model):
    schoolClass = models.CharField(max_length=20) # 班級
    className = models.CharField(max_length=20) # 班級名稱
    schoolClassChinese = models.CharField(max_length=20) # 班級名稱1
    seatNumber = models.CharField(max_length=20) # 座號
    studentID = models.IntegerField() # 學號
    name = models.CharField(max_length=30) # 姓名
    identityCard = models.CharField(max_length=30) # 身分證
    sex = models.CharField(max_length=2)  # 性別
    birth_date = models.DateField() # 出生日期