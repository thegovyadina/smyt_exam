from django.conf.urls import patterns, include, url
from django.contrib import admin
from dynamic_models.views import HomePageView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='main_page')
)