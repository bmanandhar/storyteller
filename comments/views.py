from django.shortcuts import render,redirect
from .models import Comment,Like
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
from django.views.decorators.csrf import csrf_exempt # to bypass csrf securit


@login_required 
def incrementLike(request,pk):
    cursor = connection.cursor()
    cursor.execute("SELECT id,types FROM comments_like WHERE user_id = "+str(request.user.id)+" AND story_id = "+str(pk))
    like = cursor.fetchall()  

    if len(like) > 0 :
        if like[0][1] == 'like' :
            return JsonResponse({'message':"You can't like more than once",'csrf':get_token(request)})
        else :
            cursor.execute("DELETE FROM comments_like WHERE id = "+ str(like[0][0]) )   
    cursor.execute("INSERT INTO comments_like ( story_id, user_id, types,date ) VALUES ("+str(pk)+", "+str(request.user.id)+",'like',"+str(int(time.time()))+")")
    cursor.execute("SELECT COUNT(*), types FROM comments_like WHERE story_id = "+str(pk)+" GROUP BY types")
    result = cursor.fetchall()  
    likeData = {}
    if len(result) >0 :
        for r in result :
            likeData[r[1]] = r[0]
    return JsonResponse({'message':"sucess","data":likeData,'csrf':get_token(request)})
@login_required 
def incrementDislike(request,pk):
    cursor = connection.cursor()
    cursor.execute("SELECT id,types FROM comments_like WHERE user_id = "+str(request.user.id)+" AND story_id = "+str(pk))
    like = cursor.fetchall()  

    if len(like) > 0 :
        if like[0][1] == 'dislike' :
            return JsonResponse({'message':"You can't like more than once",'csrf':get_token(request)})
        else :
            cursor.execute("DELETE FROM comments_like WHERE id = "+ str(like[0][0]) )   
    cursor.execute("INSERT INTO comments_like ( story_id, user_id, types,date ) VALUES ("+str(pk)+", "+str(request.user.id)+",'dislike',"+str(int(time.time()))+")")
    cursor.execute("SELECT COUNT(*), types FROM comments_like WHERE story_id = "+str(pk)+" GROUP BY types")
    result = cursor.fetchall()  
    likeData = {}
    if len(result) >0 :
        for r in result :
            likeData[r[1]] = r[0]
    return JsonResponse({'message':"sucess","data":likeData,'csrf':get_token(request)})
@login_required 
def createComment(request) :
    if request.method =='POST' :
        body = request.POST.get('body','')
        story = request.POST.get('story','')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO comments_comment ( story_id, user_id, body,date ) VALUES ("+str(story)+", "+str(request.user.id)+",'"+body+"',"+str(int(time.time()))+") RETURNING id")
        lastid = cursor.fetchone()[0]

        cursor.execute("SELECT c.id,c.body,c.date,u.first_name,p.profile_pic FROM comments_comment c INNER JOIN auth_user u ON u.id = c.user_id INNER JOIN user_userprofile p ON p.user_id = c.user_id WHERE c.id = "+str(lastid) )
        c = cursor.fetchone()  
      
        commentData = {
            'id'    :c[0],
            'body'  : c[1],
            'date'  : datetime.datetime.fromtimestamp(int(c[2])).strftime('%B-%d-%Y'),
            'name'  : c[3],
            'pic'   : c[4],
            'edit'  : 'edit',
            'baseurl' : request.get_host()
        }

       

        return JsonResponse({'message':'Comment added sucesfully','csrf':get_token(request),'comment':commentData})
    else :
        return HttpResponse(status=403)
        

