from django.conf.urls import url
from . import views


app_name = 'app'
urlpatterns = [

    url(r'^$', views.MainPage.as_view(), name="main_page"),
    url(r'^registration$', views.RegistrationView.as_view(), name="registration"),
    url(r'^profile/(?P<pk>\d+)/', views.CustomUserDetailView.as_view(), name="user_detail"),
    url(r'^user_update/(?P<pk>\d+)/', views.UserUpdate.as_view(), name="user_update"),



]