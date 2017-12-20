from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    #return HttpResponse("Hello, world. This is information retrieval example")

    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)



