# import patterns as patterns
from django.conf.urls import url
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('forgot/', views.forgot, name='forgot'),
    url(r'logout/$', views.pagelogout, name='logout'),
    url(r'permission/(?P<pk>\d+)$', views.permission, name='perm'),
    url(r'groups/$', views.groups, name='group'),
    url(r'permission-save-api/$', views.permission_post, name="save-permission"),

]
