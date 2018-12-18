from django.shortcuts import render
from .models import UserProfile
# Create your views here.

def home(request):
     print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
     print(request.user.is_authenticated )
     return render(request,'page/base.html')
   




