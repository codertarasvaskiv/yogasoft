from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^activate/(?P<key>.+)$', activation, name='activation'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include("app.urls")),
    url(r'^', include("app.urls")),
    url(r'^i18n/', include('django.conf.urls.i18n')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)