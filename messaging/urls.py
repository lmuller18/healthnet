from django.conf.urls import include, url

from . import views

app_name = 'messaging'
urlpatterns = [
    url(r'^$', views.MessagingView, name='index'),
    url(r'^new/', views.New_Message, name='new'),
    url(r'^(?P<m_id>[0-9]+)/view/', views.View_Message, name='view'),
    url(r'^(?P<parent_id>[0-9]+)/respond/', views.Respond, name='respond'),
    url(r'^(?P<m_id>[0-9]+)/delete/', views.Delete_Message, name='delete'),
]
