from django import contrib
from django.shortcuts import render,redirect,reverse
from django.shortcuts import HttpResponse,HttpResponseRedirect
from adminCT.models import cust_address, cust_phone_number
from Colourthreads.settings import MEDIA_URL
from adminCT.models import AdminCT
from adminCT.models import Customers,Stocks
from django.contrib.auth import login, logout
from .forms import Add_AdminForm, Add_Cat_ImageForm, cust_LoginForm, SignUpForm,SignUpFormPno,SignUpFormAddress,Add_StockForm
from django.db import connection
from django.contrib import messages
from django.conf import settings
from PIL import Image 
import os
import json

# Create your views here.

def SignUpView(request, *args, **kwargs):
    context = {}
    if request.POST:
        form_1 = SignUpForm(request.POST)
        form_2 =SignUpFormPno(request.POST)
        form_3=SignUpFormAddress(request.POST)
        if form_1.is_valid() and form_2.is_valid() and form_3.is_valid() :
            cursor=connection.cursor()
            cursor.callproc('ADD_CUSTOMER',(form_1['name'].value(),form_1['email'].value(),form_1['password'].value(),form_2['phonenumber'].value(),
            form_3['address_1'].value(),form_3['address_2'].value(),form_3['city'].value(),form_3['zipcode'].value()))
            cursor.close()
            return redirect("homepage")
        else:
            context={}
            context['name_form'] = SignUpForm()
            context['pno_form']=SignUpFormPno()
            context['address_form']=SignUpFormAddress()
            return render(request, "admin/SignUp.html", context)
    else:
        context={}
        context['name_form'] = SignUpForm()
        context['pno_form']=SignUpFormPno()
        context['address_form']=SignUpFormAddress()
        return render(request, "admin/SignUp.html", context)


def LoginView(request,cid):
    context={}
    cid = int(cid)
    if cid != 0:
        user=Customers.objects.get(cid=cid)
        login(request,user)
        user.isAuthenticated=True
        context['user']=user
        cursor=connection.cursor()
        cursor.execute('select distinct scategory from Stocks')
        t=[]
        for i in cursor:
            t.append(i)
        cursor.close()
        context['t']=t
        context['media']=MEDIA_URL
        return render(request,"home/home.html",context)
    else:
        if request.POST:
            form_4=cust_LoginForm(request.POST)
            if form_4.is_valid():
                email=form_4['email'].value()
                password=form_4['password'].value()
                cursor=connection.cursor()
                a=cursor.callfunc("VALIDATE_LOGIN",str,(email,password))
                cursor.close()
                print(a)
                if a:
                    user=Customers.objects.get(cid=a)
                    user.isAuthenticated=True
                    login(request,user)
                    print("login successfull")
                    context['user']=user
                    cursor=connection.cursor()
                    cursor.execute('select distinct scategory from Stocks')
                    t=[]
                    for i in cursor:
                        t.append(i)
                    cursor.close()
                    context['t']=t
                    context['media']=MEDIA_URL
                    return render(request,"home/home.html",context)
                else:
                    messages.info(request, 'INCORRECT PASSWORD!')
                    return redirect("homepage")
        else:
            form_4=cust_LoginForm()
            context['LoginForm']=form_4
            return render(request,"admin/Login.html",context)

def LogoutView(request):
    logout(request)
    return redirect("homepage")

def AdminLogin(request,A_id):
    A_id=int(A_id)
    if A_id !=0:
        context={}
        user=AdminCT.objects.get(A_id=A_id)
        user.isAuthenticated=True
        login(request,user)
        context['user']=user
        return render(request,"admin/adminhome.html",context)
    else:
        context={}
        if request.POST:
            form_4=cust_LoginForm(request.POST)
            if form_4.is_valid():
                email=form_4['email'].value()
                password=form_4['password'].value()
                cursor=connection.cursor()
                a=cursor.callfunc("VALIDATE_LOGIN_ADMIN",str,(email,password))

                if a:
                    user=AdminCT.objects.get(A_id=a)
                    user.isAuthenticated=True
                    login(request,user)
                    print("login successfull")
                    context['user']=user
                    cursor.close()
                    return render(request,"admin/adminhome.html",context)
                else:
                    messages.info(request, 'INCORRECT PASSWORD!')
                    return redirect("homepage")
        else:
            form_4=cust_LoginForm()
        context['LoginForm']=form_4
        return render(request,"admin/Login.html",context)


def AddAdmin(request,A_id):
    user=AdminCT.objects.get(A_id=A_id)
    context={}
    context['user']=user
    if request.POST:
        form_1 = Add_AdminForm(request.POST)
        if form_1.is_valid():

            cursor=connection.cursor()
            cursor.callproc('ADD_ADMIN',(form_1['name'].value(),form_1['email'].value(),form_1['password'].value(),form_1['phonenumber'].value()))

            cursor.close()
            return redirect("http://127.0.0.1:8000/login/admin/"+str(user.A_id))
            
        else:
            context['user']=user
            context['Add_Adminform'] = Add_AdminForm()
            return render(request, "admin/AdminSignUp.html", context)
    else:
        context['user']=user
        context['Add_Adminform'] = Add_AdminForm()
        return render(request, "admin/AdminSignUp.html", context)

def get_stock_image_filepath(ID ):
    DirectoryPath = f"media/{ID}.jpg"
    return DirectoryPath

def Add_Product(request,A_id):
    user=AdminCT.objects.get(A_id=A_id)
    context = {}
    context['user']=user
    if request.POST:
        form_1 = Add_StockForm(request.POST,request.FILES)
        if form_1.is_valid() :
            cursor=connection.cursor()
            a=cursor.callfunc('ADD_STOCKS',int,(form_1['name'].value(),form_1['category'].value().upper(),form_1['quantity'].value(),form_1['price'].value()
            ,form_1['description'].value()))
            im1=im1 = Image.open(form_1['image'].value()) 
            im1 = im1.save(get_stock_image_filepath(a))
            cursor.close()
            return redirect("http://127.0.0.1:8000/login/admin/"+str(user.A_id))
        else:
            context['form'] = Add_StockForm()
            return render(request, "admin/addproduct.html", context)
    else:
        context['form'] = Add_StockForm()
        return render(request, "admin/addproduct.html", context)

def Check_Stock(request,A_id):
    user=AdminCT.objects.get(A_id=A_id)
    login(request,user)
    context = {}
    context['user']=user
    cursor=connection.cursor()
    cursor.execute('select distinct sid,qty from less_stock ')
    t=[]
    for i in cursor:
        t.append(i)
    cursor.close()
    context['t']=t
    print(t)
    context['media']=MEDIA_URL
    return render(request,"admin/check_stock.html",context)

def Add_Cat_Image(request,A_id):
    user=AdminCT.objects.get(A_id=A_id)
    context = {}
    context['user']=user
    if request.POST:
        form_1 = Add_Cat_ImageForm(request.POST,request.FILES)
        if form_1.is_valid() :
            im1=im1 = Image.open(form_1['image'].value())
            old_pic = get_stock_image_filepath(form_1['category'].value())
            # os.remove(old_pic)
            im1 = im1.save(get_stock_image_filepath(form_1['category'].value()))
            return redirect("http://127.0.0.1:8000/login/admin/"+str(user.A_id))
        else:
            context['form'] = Add_Cat_ImageForm()
            return render(request, "admin/addproduct.html", context)
    else:
        context['form'] = Add_Cat_ImageForm()
        return render(request, "admin/addproduct.html", context)
    
def Disp_by_Category(request,CID,CAT):
    context = {}
    CID =int(CID)
    if CID != 0:
        user=Customers.objects.get(cid=CID)
        login(request,user)
        user.isAuthenticated=True
        context['user']=user
    cursor=connection.cursor()
    cursor.execute("select * from Stocks where sqty>0 and scategory ='%s'" %CAT)
    t=[]
    for i in cursor:
        t.append(i)
    cursor.close()
    context['t']=t
    context['media']=MEDIA_URL
    return render(request,"admin/Display_Cat.html",context)



def back(request,A_id):
    user=AdminCT.objects.get(A_id=A_id)
    login(request,user)
    context = {}
    context['user']=user  
    return redirect("http://127.0.0.1:8000/login/admin/"+str(user.A_id))  

def back_Cust(request,cid):
    user=Customers.objects.get(cid=cid)
    login(request,user)
    context={}
    context['user']=user
    return redirect("http://127.0.0.1:8000/login/"+str(cid))  

def like_button(request,cid,sid,cat):
    context={}
    user=Customers.objects.get(cid=cid)
    login(request,user)
    cursor=connection.cursor()
    cursor.callproc('ADD_TO_WISHLIST',(cid,sid))
    cursor.close()
    context['user']=user
    return redirect("http://127.0.0.1:8000/{cid}/{cat}".format(cid=cid,cat=cat))

def view_wishlist(request,cid):
    context={}
    user=Customers.objects.get(cid=cid)
    login(request,user)
    user.isAuthenticated=True
    context['user']=user
    cursor=connection.cursor()
    cursor.execute("select distinct sid from Wishlist where cid = '%s'" %cid)
    t=[]
    for i in cursor:
        t.append(i[0])
    s=[]
    for i in t:
        cursor.execute("select * from Stocks where sid = '%s'" %i)
        for j in cursor:
            s.append(j)
    context['s']=s
    cursor.close()
    context['media']=MEDIA_URL
    return render(request,"admin/wishlist.html",context)

def remove_wishlist(request,cid,sid):
    context={}
    user=Customers.objects.get(cid=cid)
    login(request,user)
    user.isAuthenticated=True
    context['user']=user
    cursor=connection.cursor()
    cursor.execute("delete from Wishlist where sid = {sid} and cid ={cid}".format(cid=cid,sid=sid))
    connection.commit()
    cursor.close()
    return redirect("http://127.0.0.1:8000/wishlist/{cid}".format(cid=cid))
    
def add_cart(request,cid,sid,cat):
    context={}
    user=Customers.objects.get(cid=cid)
    login(request,user)
    cursor=connection.cursor()
    cursor.callproc('ADD_CART',(cid,sid))
    cursor.close()
    context['user']=user
    return redirect("http://127.0.0.1:8000/{cid}/{cat}".format(cid=cid,cat=cat))

def view_cart(request,cid):
    context={}
    user=Customers.objects.get(cid=cid)
    login(request,user)
    user.isAuthenticated=True
    context['user']=user
    cursor=connection.cursor()
    cursor.execute("select distinct sid from CART where cid = '%s'" %cid)
    t=[]
    for i in cursor:
        t.append(i[0])
    s=[]
    for i in t:
        cursor.execute("select * from Stocks where sid = '%s'" %i)
        for j in cursor:
            s.append(j)
    context['s']=s
    cursor.close()
    context['media']=MEDIA_URL
    return render(request,"admin/cart.html",context)

def order_summary(request,cid,sid):
    context={}
    user=Customers.objects.get(cid=cid)
    user_pno=cust_phone_number.objects.get(customerid=cid)
    user_add=cust_address.objects.get(customer_id=cid)
    user.isAuthenticated=True
    context['user']=user
    context['user_pno']=user_pno
    context['user_add']=user_add
    cursor=connection.cursor()
    cursor.execute("select distinct sid from CART where cid = {cid} and sid = {sid}".format(cid=cid,sid=sid))
    t=[]
    for i in cursor:
        t.append(i[0])
    s=[]
    for i in t:
        cursor.execute("select * from Stocks where sid = '%s'" %i)
        for j in cursor:
            s.append(j)
    context['s']=s
    context['media']=MEDIA_URL
    return render(request,"admin/order_summary.html",context)

def place_order(request,cid,sid):
    context={}
    user=Customers.objects.get(cid=cid)
    login(request,user)
    cursor=connection.cursor()
    cursor.callproc('PLACE_ORDER',(cid,sid))
    cursor.execute("delete from CART where sid = {sid} and cid ={cid}".format(cid=cid,sid=sid))
    connection.commit()
    cursor.close()
    context['user']=user
    return redirect("http://127.0.0.1:8000/login/"+str(cid))

def view_orders(request,cid):
    context={}
    user=Customers.objects.get(cid=cid)
    login(request,user)
    user.isAuthenticated=True
    context['user']=user
    cursor=connection.cursor()
    cursor.execute("select sid from Orders where cid = '%s'" %cid)
    t=[]
    for i in cursor:
        t.append(i[0])
    s=[]
    for i in t:
        l=[]
        stock_details=Stocks.objects.get(sid=i)
        l.append(stock_details.sid)
        l.append(stock_details.sname)
        l.append(stock_details.sprice)
        l.append(stock_details.sdescription)
        s.append(l)
    context['s']=s
    cursor.close()
    context['media']=MEDIA_URL
    return render(request,"admin/orders.html",context)

def view_all_orders(request,aid):
    context={}
    aid=int(aid)
    user=AdminCT.objects.get(A_id=aid)
    login(request,user)
    context['user']=user
    cursor=connection.cursor()
    cursor.execute('select cid,sid from Orders')
    t=[]
    for i in cursor:
        t.append(i)
    S=[]
    print(t)
    for i in range(len(t)):
        l=[]
        user_name=Customers.objects.get(cid=t[i][0])
        print(user_name.cname)
        l.append(user_name.cname)
        l.append(user_name.cemail)
        user_pno=cust_phone_number.objects.get(customerid=t[i][0])
        l.append(user_pno.phone_number)
        user_add=cust_address.objects.get(customer_id=t[i][0])
        l.append(user_add.address1)
        l.append(user_add.address2)
        l.append(user_add.city)
        l.append(user_add.zipcode)
        stock_details=Stocks.objects.get(sid=t[i][1])
        l.append(stock_details.sid)
        l.append(stock_details.sname)
        S.append(l)
    cursor.close()
    context['s']=S
    context['media']=MEDIA_URL
    return render(request,"admin/view_order_all.html",context)


    

    
    

        

    





