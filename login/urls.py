from django.conf.urls import include, url

from . import views

app_name = 'login'

urlpatterns = [
    url(r'^$', views.LoginView, name='login'),
]