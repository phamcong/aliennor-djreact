from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.UpdateView.as_view(),
        name='update'),  # /tweet/1/update
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteView.as_view(),
        name='delete'),  # /tweet/1/update
    url(r'^(?P<id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^user/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^mechanisms/$', views.mechanism_list, name='mechanism_list'),
    url(r'^upload/csv/$', views.upload_csv, name='upload_csv'),
    url(r'^upload/json/$', views.upload_json, name='upload_json'),
]
