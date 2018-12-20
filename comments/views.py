from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Comment
# from story.models import Story

# Create your views here.

def index(request):
    comments = Comment.objects.all()
    return render(request, 'page/comment.html', {'comments': comments})

def one_comment(request, id):
    comment = Comment.objects.get(id=id)
    return render(request, 'page/comment.html', {'comment': comment})

@csrf_exempt
def createComment(request):  #everything comes from models.py
    if request.method == 'POST':
        comment = Comment(
            post = request.POST['post'],
            comment = request.POST['comment'],
            user = request.POST['user'],
            date = request.POST['date']
        )
        comment.save()
    return render(request,'page/comment.html', {'comment': comment})

@csrf_exempt
def editComment(request, pk):
    if request.method == 'POST' and user == Comment.user:
       return redirect('/')

@csrf_exempt
def updateComment(request, pk):
    comment = Comment.objects.get(id)
    comment.post = request.POST['post'],
    comment.comment = request.POST['comment'],
    comment.user = request.POST['user'],
    comment.date = request.POST['date']
    comment.save()
    return redirect('/')

@csrf_exempt
def deleteComment(request, pk):
    comment = Comment.objects.delete(id=id)
    comment.delete()
    return redirect('/')
