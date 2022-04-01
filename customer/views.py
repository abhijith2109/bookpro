from django.shortcuts import render,redirect
from owner.models import Books
from django.views.generic import View
from customer.forms import UserRegistrationForm,LoginForm,PasswordResetForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.

class customerIndex(View):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.all()
        return render(request,"cust_home.html",{"books":qs})

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=UserRegistrationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        else:
            return render(request,"signup.html",{"form":form})


class SiginInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                print("Login success")
                login(request,user)
                return redirect("custhome")

            else:

                print("login failed")
                return render(request,"signin.html",{"form":form})

def signout(request):
    logout(request)
    return redirect("signin")

class PasswordResetView(View):
    def get(self,request):
        form=PasswordResetForm()
        return render(request,"passwordreset.html",{"form":form})
    def post(self,request):
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("oldpassword")
            newpassword = form.cleaned_data.get("newpassword")
            user=authenticate(request,username=request.user,password=oldpassword)
            if user:
                user.set_password(newpassword)
                user.save()
                return redirect("signin")
            else:
                return render(request, "passwordreset.html", {"form": form})
        else:
            return render(request, "passwordreset.html", {"form": form})



