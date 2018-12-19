from django.shortcuts import render,redirect
from .models import Story
from user.models import UserProfile
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time
# from django.middleware import csrf
#      print(csrf.get_token(request))
import re
import datetime

from django.db import connection
# Create your views here.

def storypage(request) :
     return render(request,'story/story.html',{'baseurl':request.get_host() })

def allstory(request,pk):
   
    cursor = connection.cursor()
    cursor.execute('SELECT id,body,title,date,user_id FROM story_story  ORDER BY date DESC LIMIT 10 OFFSET '+ str(pk))
    stories = cursor.fetchall()   
    data = []
    for story in stories :
        cursor.execute('SELECT profile_pic FROM user_userprofile WHERE user_id='+ str(story[4]))
        usr = cursor.fetchall()   
       
        usrData = {
            "id":story[4],
            "pic" : "default.png"
        }
        if len(usr) > 0 :
            usrData['pic'] = usr[0][0]
       
        data.append(
            {
                'id':story[0],
                'body':story[1][:500],
                'title':story[2],
                'date':datetime.datetime.fromtimestamp(int(story[3])).strftime('%B-%d-%Y'),
                'user_id' : usrData
            }
        )
    return JsonResponse({"stories": data })


@login_required
def userstory(request,pk):
    cursor = connection.cursor()
    cursor.execute('SELECT id,body,title,date,user_id FROM story_story WHERE user_id= '+ str(request.user.id)+' ORDER BY date DESC LIMIT 10 OFFSET '+ str(pk))
    stories = cursor.fetchall()   
    data = []
    for story in stories :
        cursor.execute('SELECT profile_pic FROM user_userprofile WHERE user_id='+ str(story[4]))
        usr = cursor.fetchall()   
       
        usrData = {
            "id":story[4],
            "pic" : "default.png"
        }
        if len(usr) > 0 :
            usrData['pic'] = usr[0][0]
       
        data.append(
            {
                'id':story[0],
                'body':story[1][:500],
                'title':story[2],
                'date':datetime.datetime.fromtimestamp(int(story[3])).strftime('%B-%d-%Y'),
                'user_id' : usrData
            }
        )
    return JsonResponse({"stories": data })

@login_required
def createstory(request):
    if request.method == 'GET':
        return render(request,'story/new_story.html',{'baseurl':request.get_host() })
    elif request.method == 'POST':        
        story = Story.objects.create( user=request.user,body=request.POST.get('body'),title=request.POST.get('title'),date = int(time.time()))
        if story :
            return JsonResponse({"message":'sucess' })
        else :
            return JsonResponse({"message":'fail' })

@login_required          
def editstory(request,pk):

    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute('SELECT id,title,body FROM story_story WHERE user_id= '+ str(request.user.id)+' AND id='+str(pk))
        story = cursor.fetchall()  
        data = {}
        if len(story) > 0 :
            data['id']      = story[0][0]
            data['title']   = story[0][1]
            data['body']    = story[0][2]
        return render(request,'story/edit_story.html',{'data': data })

    elif request.method == 'POST':
        title    = request.POST.get('title','')
        body     = request.POST.get('body','')
        cursor = connection.cursor()
        cursor.execute("UPDATE story_story SET title = '"+title+"' , body = '"+body+"' WHERE id="+str(pk))
         
        cursor.execute('SELECT id,title,body,date,user_id FROM story_story WHERE user_id= '+ str(request.user.id)+' AND id='+str(pk))
        story = cursor.fetchall()  
       
        data = {
            'id':story[0][0],
            'title':story[0][1],
            'body':story[0][2][:500],            
            'date':datetime.datetime.fromtimestamp(int(story[0][3])).strftime('%B-%d-%Y')
        }
       
        if len(story) > 0 :
            cursor.execute('SELECT profile_pic FROM user_userprofile WHERE user_id='+ str(request.user.id))
            usr = cursor.fetchall()   
            usrData = {
                "id":pk,
                "pic" : 'http://'+str(request.get_host())+'/media/userpic/'+"default.png"
            }
            if len(usr) > 0 :
                usrData['pic'] = 'http://'+str(request.get_host())+'/media/userpic/'+usr[0][0]
            data['user_id'] = usrData;   
      
        return JsonResponse({'message':'sucess','data':data})
       



def deleteStory(request, pk):
    return render(request,'story/story.html',{'baseurl':request.get_host() })

def specific_story(request,pk):
    return render(request,'story/specific_story.html',{'baseurl':request.get_host() })
    
