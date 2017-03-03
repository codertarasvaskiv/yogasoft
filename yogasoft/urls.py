from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url('^accounts/', include('django.contrib.auth.urls')),

    url(r'^password_reset', auth_views.password_reset,
        {'template_name': '../templates/registration/password_reset.html'}, name="password_reset"),
    url(r'^resetpassword/passwordsent/$', auth_views.password_reset_done, name='password_reset_done'),
    url('', include('social_django.urls', namespace='social')),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include("app.urls")),
    url(r'^', include("app.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)