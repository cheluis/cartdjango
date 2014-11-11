from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from shop import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cartdjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', views.Index.as_view(), name="index"),
    url(r'^publication/(?P<pk>\d+)/$', views.PublicationDetail.as_view(), name="pub_detail"),

) 


urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name' : 'login.html'},
        name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/index/'}, name='mysite_logout'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)