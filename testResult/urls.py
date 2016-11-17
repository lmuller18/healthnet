from django.conf.urls import include, url

from . import views

app_name = 'testResult'
urlpatterns = [
    url(r'^$', views.ListView, name='index'),
    url(r'^(?P<t_id>[0-9]+)/edit/', views.Edit_Result,name='Edit_Result'),
    url(r'^new/', views.Create_Result, name='Create_Result'),
    url(r'^(?P<t_id>[0-9]+)/view/', views.View_Result, name='View_Result'),
    url(r'^(?P<t_id>[0-9]+)/delete/', views.Delete_Result, name='Delete_Result')
]
