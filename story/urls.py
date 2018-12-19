from django.urls import path
from . import views

urlpatterns=[
    path('',views.storypage,name="story"),
    path('<int:pk>', views.specific_story,name="story"),
    path('all/<int:pk>',views.allstory,name="allstory"),
    path('user/<int:pk>',views.userstory,name="userstory"),
    path('<int:pk>/edit',views.editstory,name="editstory"),
    path('create',views.createstory,name="create_story"),
]