from django.urls import include, path, re_path
from django.contrib import admin

from main import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'FMPusher.views.home', name='home'),
    # url(r'^FMPusher/', include('FMPusher.foo.urls')),
    re_path(r'^$', views.home),
    re_path(r'^device$', views.device),
    re_path(r'^clkcount/(?P<pk>\d+)$', views.clkcountpk),
    re_path(r'^clkcount/(?P<url>.+)$', views.clkcount),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    re_path(r'^captcha/', include('captcha.urls')),
]