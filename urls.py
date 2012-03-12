from django.conf.urls.defaults import patterns, include, url
from settings import STATIC_URL


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'CoreBuilder.corebuilder.views.home', name='home'),
    url(r'^CoreBuilder/corebuilder/', 'CoreBuilder.corebuilder.views.home'),
    url(r'^targetchanged', 'CoreBuilder.corebuilder.views.target_changed'),
    url(r'^viewchanged', 'CoreBuilder.corebuilder.views.view_changed'),
    url(r'^pkgchanged', 'CoreBuilder.corebuilder.views.pkg_changed'),
    url(r'^verchanged', 'CoreBuilder.corebuilder.views.get_metadata'),
    url(r'^merge', 'CoreBuilder.corebuilder.views.merge'),
    url(r'^unmerge', 'CoreBuilder.corebuilder.views.unmerge'),

    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': STATIC_URL}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)
