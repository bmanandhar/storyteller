from django.urls import path
from . import views

urlpatterns=  [
    # url(r'^$', views.index),
    path('create', views.create),
    # url(r'edit/(?P<id>\d+)$', views.edit),
    # url(r'update/(?P<id>\d+)$', views.update),
    # url(r'delete/(?P<id>\d+)$', views.destroy)

]