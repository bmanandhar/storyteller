from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('one_comment', views.one_comment, name='one_comment'),
    path('create/', views.createComment, name='createComment'),
    path('editComment/<int:id>', views.editComment, name='editComment'),
    path('updateComment/<int:id>', views.updateComment, name='updateComment'), 
    path('deleteComment/<int:id>', views.deleteComment, name='deleteComment')
    ]
