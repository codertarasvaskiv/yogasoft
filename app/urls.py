from django.conf.urls import url
from . import views


app_name = 'app'
urlpatterns = [

    url(r'^$', views.MainPage.as_view(), name="main_page"),
    url(r'start_project/$', views.StartProjectView.as_view(), name="start_project"),

]