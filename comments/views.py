from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
@csrf_exempt
# Create your views here.

def createComment(request):
    if request.method == 'POST':
        print('zzz+zzzz+zzz')
        print(request.POST)
        return HttpResponse('Got it!')

def updateComment(request):
    if request.method == 'POST':
        print('yy-yy-yy-yy')
        print(request.POST)
        return HttpResponse('Got it!')

def deleteComment(request):
    if request.method == 'POST':
        PRINT('xx..xxx..xx')
        print((request.POST))
        return HttpResponse('deleted')