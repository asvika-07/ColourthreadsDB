
from django.shortcuts import render
from django.db import connection
from Colourthreads.settings import MEDIA_URL

# Create your views here.
def Homepage(request,*args,**kwargs):
    context={}
    cursor=connection.cursor()
    cursor.execute('select distinct scategory from Stocks')
    t=[]
    for i in cursor:
        t.append(i)
    cursor.close()
    context['t']=t
    context['media']=MEDIA_URL
    return render(request, "home\home.html",context)