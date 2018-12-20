from django.shortcuts import render,redirect
from .models import Story
from user.models import UserProfile
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time
import re
import datetime
from django.db import connection
from django.middleware.csrf import get_token

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
    cursor = connection.cursor()
    cursor.execute('SELECT s.id,s.title,s.body,s.date,s.user_id,u.profile_pic,a.first_name FROM story_story s INNER JOIN user_userprofile u ON u.user_id= s.user_id INNER JOIN auth_user a ON u.user_id = a.id AND s.id ='+str(pk))
    story = cursor.fetchall()  
    
    if len(story) > 0 :
        data = {
            'id'    : story[0][0],
            'title' :story[0][1],
            'body'  :story[0][2],          
            'date'  :datetime.datetime.fromtimestamp(int(story[0][3])).strftime('%B-%d-%Y'),
            'user_id':story[0][4],
            'pic'   :story[0][5],
            'name'  :story[0][6]   
        }     
        #adding like dislike 
        cursor.execute("SELECT COUNT(*), types FROM comments_like WHERE story_id = "+str(pk)+" GROUP BY types")
        result = cursor.fetchall()  
        likeData = {'like':0,'dislike':0}
        if len(result) >0 :
            for r in result :
                likeData[r[1]] = r[0]

        data['likes'] = likeData
        #adding comments
        cursor.execute("SELECT c.id,c.body,c.date,u.first_name,p.profile_pic FROM comments_comment c INNER JOIN auth_user u ON u.id = c.user_id INNER JOIN user_userprofile p ON p.user_id = c.user_id WHERE story_id = "+str(pk) + ' ORDER BY c.date DESC ')
        comments = cursor.fetchall()  
        commentData = []
        
        if len(comments) >0 :
            for c in comments :
                commentData.append({
                    'id'    :c[0],
                    'body'  : c[1],
                    'date'  : datetime.datetime.fromtimestamp(int(c[2])).strftime('%B-%d-%Y %H:%M:%S'),
                    'name'  : c[3],
                    'pic'   : c[4],
                    'edit'  : data['user_id'] == request.user.id and 'edit' or 'noedit'
                })

        data['comments'] = commentData
       
        return render(request,'story/specific_story.html',{'baseurl':request.get_host(),'data':data,'csrf':get_token(request) })
    else :
        return HttpResponse(status=403)
    
