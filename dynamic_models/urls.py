from django.conf.urls import patterns, include, url
from views import HomePageView, ModelView


urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='main_page'),
    url(r'^model/$', ModelView.as_view(), name='get_model'),
)