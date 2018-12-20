from django.urls import path
from . import views

urlpatterns=   [
    path('', views.index, name='index'),
    path('details', views.details, name="details"),
    path('create', views.create, name='create'),
    path('edit', views.edit, name='edit'),
    path('update', views.update, name="update"),
    path('delete', views.delete, name="delete")
    
]