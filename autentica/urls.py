from django.conf.urls import patterns, include, url
from django.contrib import admin

from cliente import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autentica.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.inicio),
    url(r'^pedir-autorizacion/', views.pedir_autorizacion),
    url(r'^pedir-token/', views.pedir_token),
)
