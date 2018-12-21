from django.shortcuts import render,redirect

def notfound(request) :
    return render(request,'page/notfound.html')