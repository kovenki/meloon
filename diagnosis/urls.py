from django.conf.urls import url

from . import views

app_name = 'diagnosis'
urlpatterns = [
    # ex: /diagnosis/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /diagnosis/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /diagnosis/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /diagnosis/5/vote/
    url(r'^(?P<pk>[0-9]+)/vote/$', views.vote, name='vote'),
]
