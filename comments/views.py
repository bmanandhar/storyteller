from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Comment

# Create your views here.

@csrf_exempt
def createComment(request):
		return render(request, 'page/comment.html')

@csrf_exempt
def updateComment(request, id):
    comment = comment.objects.get(id=id)
    comment.user = request.POST['user']
    comment.body = request.POST['comment']
    story.date = request.POST['date']
    stroy.title = request.POST['title']
    story.save()
    return redirect('/')


@csrf_exempt
def update(request, id):
    story = Story.objects.get(id=id)
    story.user = request.POST['user']
    story.body = request.POST['body']
    story.date = request.POST['date']
    stroy.title = request.POST['title']
    story.save()
    return redirect('/')
@csrf_exempt
def deleteComment(request):
    if request.method == 'POST':
        return HttpResponse('Got deletes!')