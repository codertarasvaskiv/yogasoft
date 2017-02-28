from django.conf.urls import url
from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.MainPage.as_view(), name="main_page"),

    url(r'^test', views.Test.as_view(), name="test"),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),



    url(r'^index$', views.IndexPage.as_view(), name="index_page"),
    url(r'^login/$', views.LoginPage.as_view(), name="login_page"),
    url(r'^access_required/$', views.AccessRequired.as_view(), name='access_required_page'),
    url(r'start_project/$', views.StartProjectView.as_view(), name="start_project"),
    url(r'blog/(?P<pk>\d+)/$', views.BlogDetailView.as_view(), name='blog_detail_view')

]
