from django.conf.urls import url
from . import views


app_name = 'app'
urlpatterns = [

    url(r'^$', views.MainPage.as_view(), name="main_page"),
    url(r'^login/$', views.LoginPage.as_view(), name="login_page"),
    url(r'^access_required/$', views.AccessRequired.as_view(), name='access_required_page'),
    url(r'start_project/$', views.StartProjectView.as_view(), name="start_project"),
    url(r'testimonials/$', views.Testimonials.as_view(), name="testimonials"),
    url(r'testimonials_admin/$', views.TestimonialsAdmin.as_view(), name="testimonials_admin"),
    url(r'testimonials_admin/(?P<testimonial_id>[0-9]+)/$', views.TestimonialsAdmin.as_view(), name="testimonials_admin"),
]