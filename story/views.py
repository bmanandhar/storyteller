from django.shortcuts import render, redirect
from .models import Story
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def index(request):
    storys = Story.objects.all()
    context = {
        'storys':storys
        }
    return render(request, 'story/index.html', context)

def details(request, id=None):
    context = { 'stroy' :story}
    story = Story.objects.get(id=id)
    return render(request, 'story/index.html', context) 


@csrf_exempt
def create(request):
    # print request.POST
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    if request.method == 'POST': 
        story = Story(
        user=request.POST['user'], 
        body=request.POST['body'],
        date=request.POST['date'],
        title=request.POST['title'],)
        stry =  story.save()
        print(stry)
        return redirect('')
    else:
        print(story.error)
        return JsonResponse({'foo':'bar'})


def edit(request, id):
    story = Story.objects.get(id=id)
    context = {
        'story':story
        }
    return render(request, 'story/edit.html', context )

def update(request, id):
    story = Story.objects.get(id=id)
    story.user = request.POST['user']
    story.body = request.POST['body']
    story.date = request.POST['date']
    stroy.title = request.POST['title']
    story.save()
    return redirect('/story/')

def delete(request, id):
    story = Story.objects.delete(id=id)
    story.delete()
    return redirect('/story/')
    print('story deleted')
    return HttpResponseRedirect('/story/')

