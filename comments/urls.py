from django.urls import path
from . import views

urlpatterns=[ 
    path('create', views.createComment)
    path('<int:pk>/update', views.updateComment)   
]