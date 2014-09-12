from django.conf.urls import patterns, include, url
from views import HomePageView, GetModelView


urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='main_page'),
    url(r'^get_model/$', GetModelView.as_view(), name='get_model'),
)