from django.conf.urls import include, url

from . import views

app_name = 'registration'

urlpatterns = [
    url(r'^$', views.PatientReg, name='index'),
    url(r'^admin/', views.AdminReg, name='admin'),
    
    # to edit another user's profile, pass their private key in url
    url(r'^edit/(.*)/', views.PatientProfileEdit, name='edit'),
    
    # patients editing their own profiles don't use pk
    url(r'^edit/', views.PatientProfileEdit, name='edit'),
    
    # to see another user's profile, pass their private key in url
    url(r'^profile/(.*)/', views.PatientProfileView, name='profile'),
    
    # patients viewing their own profiles don't use pk
    url(r'^profile/', views.PatientProfileView, name='profile'),
    
    url(r'^admit/(.*)/', views.PatientAdmissionView, name='admit'),
    
    url(r'^transfer/(.*)/', views.PatientTransferView, name='transfer'),
    
    url(r'^export/', views.ExportPatientView, name='export'),
    url(r'^download/', views.DownloadFile, name='download'),
]
