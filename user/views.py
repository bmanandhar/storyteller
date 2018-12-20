from django.shortcuts import render,redirect
from .models import UserProfile
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware import csrf
from django.db import connection
from django.contrib.auth import hashers
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
     cursor = connection.cursor()
     cursor.execute("SELECT u.first_name,u.email,u.username, p.profile_pic FROM auth_user u INNER JOIN user_userprofile p ON p.user_id = u.id WHERE u.id = "+str(request.user.id))
     user = cursor.fetchone()  
     userData = {
          "name"    :user[0],
          "email"   :user[1],
          "username":user[2],
          "pic"     :user[3],
     }
     
     return render(request,'page/profile.html',{'baseurl':request.get_host(),'csrf':csrf.get_token(request),"user":userData })
    
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

@login_required
def userProfileEdit(request) :
     if request.method == 'POST':
          
          name           = request.POST.get('name','')
          email          = request.POST.get('email','')
          username       = request.POST.get('username','')
          password       = request.POST.get('password','')
          old_password   = request.POST.get('old_password','')
          error          =  'Sucessfully updated user profile'

          if re.sub(r'\s+', '', name) == '' and re.sub(r'\s+', '', email) == '' and re.sub(r'\s+', '', username) == '' and re.sub(r'\s+', '', password) == '' :
               error = 'Invalid data found in field'
          else :
               cursor = connection.cursor()
               if name != '' :
                    cursor.execute("UPDATE auth_user SET first_name = '"+name+"' WHERE id = "+str(request.user.id))
               elif email != '':
                    cursor.execute("UPDATE auth_user SET email = '"+email+"' WHERE id = "+str(request.user.id))
               elif username != '' or password != '':  # if username or password                 
                    cursor.execute("SELECT password FROM auth_user WHERE id = "+str(request.user.id))
                    password = cursor.fetchone()  

                    if hashers.check_password(old_password,password[0]) == False :# hash password
                         error = 'Password not matched'
                    else :
                         if username != '': # username change
                             
                              if User.objects.filter( username = username ).exists():
                                   error = 'Username already exist'
                              else :
                                   cursor.execute("UPDATE auth_user SET username = '"+username+"' WHERE id = "+str( request.user.id ) )
                         else : # password change
                              u = User.objects.get(id = request.user.id)
                              u.set_password( password )
                              u.save()
                             
             
          return JsonResponse({'message':error,'csrf':csrf.get_token(request)})
     else :
          return HttpResponse(status=403)





