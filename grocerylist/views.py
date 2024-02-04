from django.http import HttpResponse
from django.template import loader 
from .models import GroceryList
import csv 
from django.shortcuts import render 
from django.db.models import Q

def grocerylist(request): 
    with open('output.csv','r') as file: 
        csvreader = csv.reader(file)
        for row in csvreader: 
            GroceryList.objects.create(type=row[0], name=row[1], price=row[2],rating=row[3],inlist=False)
    if 'q' in request.GET:
        q = request.GET['q']
        #mygrocerylist = GroceryList.objects.filter(type__icontains=q)
        multiple_q = Q(Q(type__icontains=q) | Q(name__icontains=q))
        mygrocerylist = GroceryList.objects.filter(multiple_q)
    else: 
        mygrocerylist = GroceryList.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'mygrocerylist': mygrocerylist,
    }
    
    return HttpResponse(template.render(context, request))
#def grocerylist(request): 
    #mygrocerylist = GroceryList.objects.all().values()
    #template = loader.get_template('index.html')
    #context = {
    #    'mygrocerylist': mygrocerylist,
    #}
    #return HttpResponse(template.render(context, request))
# Create your views here.
