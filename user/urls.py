from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('user/register',views.register,name="register"),
    path('user/logout',views.userLogout,name="logout"),
    path('user/login',views.userLogin,name="login"),
    path('user/profile',views.userProfile,name="profile"),
    path('user/profile/edit',views.userProfileEdit,name="profileedit")
   
    
]