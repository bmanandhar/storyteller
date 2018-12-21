from django.urls import path
from . import views

urlpatterns=[
    path('',views.storypage,name="story"),
    path('<int:pk>', views.specific_story,name="story"), #get particular story
    path('all/<int:pk>',views.allstory,name="allstory"),#getting all the story
    path('user/<int:pk>',views.userstory,name="userstory"),#getting all the published story by user
    path('<int:pk>/edit',views.editstory,name="editstory"),#edit story
    path('create',views.createstory,name="create_story"),
]