from django.conf.urls import url, include

from . import views

app_name = 'appointment'

urlpatterns = [
    url(r'^$', views.AppointmentView, name='index'),
    url(r'^new/', views.NewAppointment, name='new'),
    url(r'^(?P<pk>[0-9]+)/edit/', views.EditAppointment, name='edit'),
    url(r'^(?P<pk>[0-9]+)/view/', views.ViewAppointment, name='view'),
    url(r'^(?P<pk>[0-9]+)/delete/', views.DeleteAppointment, name='delete'),
]
