from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
   
    #path('', views.index, name = 'IRsearch'),
    
    #path('', views.RView, name = 'result'),
    #path('', views.RView, name = 'index'),

]


