# from django.conf.urls import url
from Facial_Recognition_App import views
from django.urls import include, re_path


app_name = 'Facial_Recognition_App'


urlpatterns = [

re_path(r'^register/$', views.register, name = 'register'),
re_path(r'^user_login/$', views.user_login, name = 'user_login'),

]
