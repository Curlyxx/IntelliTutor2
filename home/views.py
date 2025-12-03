from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    """Vista principal de la aplicación home"""
    context = {
        'page_title': 'IntelliTutor UNAM'
    }
    return render(request, 'home/index.html', context)