from django.conf.urls import include, url

from . import views

app_name = 'prescriptions'
urlpatterns = [
    url(r'^$', views.PrescriptionView, name='index'),
    url(r'^new/', views.New_Prescription, name='New_Prescription'),
    url(r'^(?P<p_id>[0-9]+)/edit/', views.Edit_Prescription, name='Edit_Prescription'),
    url(r'^(?P<p_id>[0-9]+)/view/', views.viewPrescription, name='View_Prescription'),
    url(r'^(?P<p_id>[0-9]+)/delete/', views.Delete_Prescription, name='Delete_Prescription'),
]
