from django.shortcuts import render,redirect

# Create your views here.

# CATEGORY
from backend.forms import *
def c_form(request):
    frm=CategoryForm()
    return render(request,"category_form.html",{"frm":frm})

from backend.models import *
def c_save(request):
    if request.POST:
        frm=CategoryForm(request.POST,request.FILES)
        if frm.is_valid():
            frm.save()
            return redirect(c_table)
    else:
        frm=CategoryForm()
    return render(request,"category_form.html",{"frm":frm})

def c_table(request):
    data=pro_category.objects.all()
    return render(request,"category_table.html",{"data":data})


def c_delete(request,dataid):
    data=pro_category.objects.filter(id=dataid)
    data.delete()
    return redirect(c_table)

def c_edit(request,dataid):
    edited=pro_category.objects.get(id=dataid)
    if request.POST:
        frm=CategoryForm(request.POST,request.FILES,instance=edited)
        if frm.is_valid():
            frm.save()
            return redirect(c_table)
    else:
        frm=CategoryForm(instance=edited)
    return render(request,"category_edit.html",{"frm":frm})



# PRODUCT

def pro_form(request):
    data = pro_category.objects.all()
    frm = ProductForm()
    return render(request, "product_form.html", {"frm": frm, "data": data})



def pro_save(request):
    if request.POST:
        frm=ProductForm(request.POST,request.FILES)
        if frm.is_valid():
            frm.save()
            return redirect(p_table)
    else:
        frm =ProductForm()
    return render(request,"product_form.html",{"frm":frm})

def p_table(request):
    data = protable.objects.all()
    return render(request,"product_table.html",{"data":data})

def p_delete(request,dataid):
    data=protable.objects.filter(id=dataid)
    data.delete()
    return redirect(p_table)
def p_edit(request,dataid):
    edited = protable.objects.get(id=dataid)
    if request.POST:
        frm = ProductForm(request.POST,request.FILES,instance=edited)
        if frm.is_valid():
            frm.save()
            return redirect(p_table)
    else:
        frm = ProductForm(instance=edited)
    return render(request,"product_edit.html",{"frm":frm})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")     # redirect after login
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")