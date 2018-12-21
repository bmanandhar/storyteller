from django.urls import path
from . import views

urlpatterns=[
    path('create',views.createComment,name="create"),
    path('like/story/<int:pk>',views.incrementLike,name="like"),
    path('dislike/story/<int:pk>',views.incrementDislike,name="dslike"),
    path('<int:pk>/delete',views.deleteComment,name="delete"),
]