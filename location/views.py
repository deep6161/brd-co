from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def location(req):
    return HttpResponse("this is location area file")
