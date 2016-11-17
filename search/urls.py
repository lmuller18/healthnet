from django.conf.urls import include, url

from . import views

app_name = 'registration'

urlpatterns = [
    url(r'^$', views.SearchView, name='index'),
]
