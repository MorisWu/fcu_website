from django.db import models

# Create your models here.

class citrix_log(models.Model):
    location_name = models.CharField(max_length=50) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[Application].Name
    user_name = models.CharField(max_length=50) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[User].UserName
    user_ip = models.CharField(max_length=50)  #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[Connection].ClientAddress
    application_start_date = models.DateTimeField(null = True) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[ApplicationInstance].StartDate
    user_logon_start_date = models.DateTimeField(null = True) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[ApplicationInstance].LogOnStartDate
    session_start_date = models.DateTimeField(null = True) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[Session].StartDate
    session_end_date = models.DateTimeField(null = True) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[Session].EndDate
    connection_logon_date = models.DateTimeField(null = True) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[Connection].LogOnEndDate
    application_end_date = models.DateTimeField(null = True) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[ApplicationInstance].EndDate
    application_id = models.CharField(max_length=100) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[ApplicationInstance].ApplicationId
    session_user_id = models.CharField(max_length=100) #origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[Session].UserId
    application_sessionkey = models.CharField(max_length=100)#origin label: [CitrixFCUVDIMonitoring1].[MonitorData].[ApplicationInstance].SessionKey