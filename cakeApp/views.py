from django.shortcuts import render,redirect
from django.views.generic import View
from django import forms
from cakeApp.models import Cakes
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
class CakeForm(forms.ModelForm):
    class Meta:
        model=Cakes
        fields=['name','flavour','weight','tier','colour','price','image']
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "flavour":forms.TextInput(attrs={"class":"form-control"}),
            "weight":forms.NumberInput(attrs={"class":"form-control"}),
            "tier":forms.NumberInput(attrs={"class":"form-control"}),
            "colour":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"})

        }

class RegisterForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"}),

        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class CakeCreateView(View):
    def get(self,request,*args,**kw):
        form=CakeForm()
        return render(request,"cake-create.html",{"form":form})
    def post(self,request,*args,**kw):
        form=CakeForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            Cakes.objects.create(**form.cleaned_data,user=request.user)
            messages.success(request,"cake is successfully added")
            return redirect("cake-list")
        messages.error(request,"failed-try again")
        return render(request,"cake-create.html",{"forms":form})

class CakeListView(View):
    def get(self,request,*args,**kw):
        qs=Cakes.objects.filter(user=request.user)
        return render(request,"cake-list.html",{"cakes":qs})

class CakeDetailView(View):
    def get(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Cakes.objects.get(id=id)
        return render(request,"cake-detail.html",{"cakes":qs})
    
class CakeDeleteView(View):
    def get(self,request,*args,**kw):
        id=kw.get("pk")
        Cakes.objects.get(id=id).delete()
        messages.success(request,"cake is deleted")
        return redirect("cake-list")
    
class CakeEditView(View):
    def get(self,request,*args,**kw):
        id=kw.get("pk")
        cake=Cakes.objects.get(id=id)
        form=CakeForm(instance=cake)
        return render(request,"cake-edit.html",{"form":form})
    def post(self,request,*args,**kw):
        id=kw.get("pk")
        cake=Cakes.objects.get(id=id)
        form=CakeForm(data=request.POST,instance=cake,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"successfully edited")
            return redirect("cake-detail",pk=id)
        messages.error(request,"updation failed")
        return render(request,'cake-edit.html',{"form":form})

class SignUpView(View):
    def get(self,request,*args,**kw):
        form=RegisterForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kw):
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"successfully created account")
            return redirect("signIn")
        messages.error(request,"account creation failed")
        return render(request,"register.html",{"form":form})
    

class SignInView(View):
    def get(self,request,*args,**kw):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"success")
                return redirect("cake-list")
            messages.error(request,"invalid details")
            return render(request,"login.html",{"form":form})


