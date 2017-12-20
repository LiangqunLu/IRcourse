from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.http import HttpResponseRedirect

from .forms import NameForm

import sys
sys.path.insert(0, '/Users/Leah/Downloads/django/mysite/IR/WIR')

import hw7

from hw7 import IR
import numpy as np

import os

def index(request):
    #return HttpResponse("Hello, world. This is information retrieval example")

    context = {}
    context['hello'] = 'Hello World!'
    #return render(request, 'index.html', context)

    if request.method == 'POST':

        form = NameForm(request.POST)
        if form.is_valid():

            ##make use of search content
            search_item = 'example'
            search_item = form.cleaned_data['IRsearch']
            out = IR(search_item)
            out = out.iloc[:100, :]

            context['name'] = search_item
            context['data'] = out.to_html()
            #print(out)
            return render(request, 'result.html', context )

    else:
        form = NameForm()

    return render(request, 'index.html', {'form':form})



def RView(request):
    # Use '.get('id', None)' in case you don't receive it, avoid getting error
    selected_option = request.POST.get('my_options', None)  

    if selected_option:
        # Do what you need with the variable
     	#return([one for one in range(10)])
        aa = [one for one in range(10)]

        #return HttpResponse("Hello, world." + aa)

    return render(request, 'result.html')


