from django.conf.urls import url, include

from . import views

app_name = 'log'

urlpatterns = [
    url(r'^$', views.LogView, name='index'),
]
