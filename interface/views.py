from django.shortcuts import render
from django.http import HttpResponse,Http404

# Create your views here.

def index(request):
    return render(request, "interface/index.html")

texts = ["My name is Jeff.","My name is Gary.","My name is Kyle."]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")