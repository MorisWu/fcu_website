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

'''
USE CitrixFCUVDIMonitoring1;

SELECT
       b.Name
      ,d.UserName
      ,e.ClientAddress
      ,a.StartDate
      ,e.LogOnStartDate
      ,c.StartDate
      ,c.EndDate
      ,e.LogOnEndDate
      ,a.EndDate
      ,a.ApplicationId
      ,c.UserId
      ,a.SessionKey
  FROM [CitrixFCUVDIMonitoring1].[MonitorData].[ApplicationInstance] a
      ,[CitrixFCUVDIMonitoring1].[MonitorData].[Application] b
      ,[CitrixFCUVDIMonitoring1].[MonitorData].[Session] c
      ,[CitrixFCUVDIMonitoring1].[MonitorData].[User] d
      ,[CitrixFCUVDIMonitoring1].[MonitorData].[Connection] e
where
      a.ApplicationId = b.Id
  and a.SessionKey = c.SessionKey
  and c.UserId = d.id
  and a.SessionKey = e.SessionKey


'''