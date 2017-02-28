from django.conf.urls import url
from . import views


app_name = 'app'
urlpatterns = [
    url(r'^$', views.MainPage.as_view(), name="main_page"),


    # lust testing need to delete later Taras
    url(r'^test', views.Test.as_view(), name="test"),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),



    url(r'^index$', views.IndexPage.as_view(), name="index_page"),
    url(r'^login/$', views.LoginPage.as_view(), name="login_page"),
    url(r'^access_required/$', views.AccessRequired.as_view(), name='access_required_page'),
    url(r'start_project/$', views.StartProjectView.as_view(), name="start_project"),

    url(r'^blog/(?P<pk>\d+)/add_comment/$', views.AddComment, name='add_comment'),
    url(r'^blog/(?P<pk>\d+)/add_comment/(?P<comm_pk>\d+)/$', views.add_second_comment, name='add_second_level_comment'),
    url(r'^blog/(?P<pk>\d+)/$', views.BlogDetailView.as_view(), name='blog_detail_view'),
    url(r'^blog/$', views.BlogListView.as_view(), name='blog_list_view'),
    url(r'^blog/tag/(?P<tag>[a-zA-Z0-9]+)/$', views.BlogListView.as_view(), name='blog_list_view_tag'),


]
