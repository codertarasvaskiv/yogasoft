from django.conf.urls import url
from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name="main_page"),

    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^registration$', views.register, name="registration"),
    url(r'^portfolio$', views.PortfolioListView.as_view(), name="portfolio"),
    url(r'^portfolio/(?P<pk>\d+)', views.PortfolioDetailView.as_view(), name="portfolio_detail"),
    url(r'^index/$', views.IndexPage.as_view(), name="index_page"),
    url(r'^index$', views.IndexPage.as_view(), name="index_page"),
    url(r'^access_required/$', views.AccessRequired.as_view(), name='access_required_page'),
    url(r'start_project/$', views.StartProjectView.as_view(), name="start_project"),
    url(r'testimonials/$', views.Testimonials.as_view(), name="testimonials"),
    url(r'testimonials_admin/$', views.TestimonialsAdmin.as_view(), name="testimonials_admin"),
    url(r'testimonials_admin/(?P<testimonial_id>[0-9]+)/$', views.TestimonialsAdmin.as_view(), name="testimonials_admin"),
    url(r'^blog/(?P<pk>\d+)/add_comment/$', views.AddComment, name='add_comment'),
    url(r'^blog/(?P<pk>\d+)/add_comment/(?P<comm_pk>\d+)/$', views.add_second_comment, name='add_second_level_comment'),
    url(r'^blog/(?P<pk>\d+)/$', views.BlogDetailView.as_view(), name='blog_detail_view'),
    url(r'^blog/$', views.BlogListView.as_view(), name='blog_list_view'),
    url(r'^blog/tag/(?P<tag>[a-zA-Z0-9]+)/$', views.BlogListView.as_view(), name='blog_list_view_tag'),
    url(r'^site_admin/$', views.SiteAdmin.as_view(), name='site_admin'),
    url(r'^site_admin/admin_users/$', views.AdminUsers.as_view(), name='admin_users'),
    url(r'^site_admin/edit_admin_user/(?P<user_id>[0-9]+)/$', views.EditAdminUser.as_view(), name='edit_admin_user'),
    url(r'^contact_us/$', views.ContactUsView.as_view(), name='contact_us'),




    url(r'^search_list/(?P<info>.*)$', views.SearchListAsView.as_view(), name='search'),

    url(r'^test/$', views.Test.as_view(), name='test'),
    url(r'^test2/$', views.Test2.as_view(), name='test'),


]
