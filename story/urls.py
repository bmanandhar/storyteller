from django.urls import path
from . import views

urlpatterns=  [
    path('', views.index, name='index'),
    path('create', views.create,),
    path('edit', views.edit),
    path('update', views.update),
    path('delete', views.destroy)

]