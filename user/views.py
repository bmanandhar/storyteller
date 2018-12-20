from django.shortcuts import render,redirect
from .models import UserProfile
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware import csrf
import re




# Create your views here.


def home(request):    
     errs = request.session.get('errs')
     privErrs =  errs
     if errs != None :
          del request.session['errs']
     return render(request,'page/main.html',{ 'data' : privErrs,'baseurl':request.get_host() })

@login_required
def userLogout(request) :
     logout(request)
     return redirect('home')

@login_required
def userProfile(request) :    
     return render(request,'page/profile.html',{'baseurl':request.get_host(),'csrf':csrf.get_token(request) })
    
def userLogin(request):
     if request.method == 'POST':
          errors = {}
          username = request.POST.get('username')
          password = request.POST.get('password')
          user = authenticate(username=username, password=password)
        
          if user:
               if user.is_active:
                    login(request,user)
                    return redirect('home')
               else:
                    request.session['errs'] = {"inactive":"Your account is disabled"}
                    return redirect('home')
          else:               
               request.session['errs'] = {"loginfail":"Invalid Username or Password"}
               return redirect('home')
     else:
          return HttpResponse(status=403)

def register(request) :
     if request.method == 'POST':
          errors = {}
          fullname       = request.POST.get('name','')
          email          = request.POST.get('email','')
          username       = request.POST.get('username','')
          password       = request.POST.get('password','')
          con_password   = request.POST.get('conpassword','')   

          if(re.search('^[0-9a-zA-Z\s]+$',fullname) ==  None):
               errors['name'] ="Invalid Full Name"
          
          if(re.search('^\S+@\S+$',email) ==  None):
               errors['email'] ="Invalid email address"
          elif User.objects.filter(email=email).exists():
               errors['email'] ="Email already exist"

          if(re.search('^[0-9a-zA-Z]+$',username) ==  None):
               errors['username'] ="Username only allow alpha-numeric value"   
          elif User.objects.filter(username=username).exists():
               errors['username'] ="Username already exist"
          
          if password != con_password :
               errors['password'] ="Password is not equal with conform password"

          if(len(errors) == 0) :
               user = User.objects.create_user(
                                        username=username,
                                        email=email,
                                        password=password,
                                        first_name=fullname
                                 )
               
               profile = UserProfile(profile_pic = 'default.png', user = user )
               profile.save()
               login(request,user)
               return redirect('home' )
          else :
               request.session['errs'] = errors
               return redirect('home' )
     else:
          return HttpResponse(status=403)
   



