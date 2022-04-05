from django.shortcuts import render,redirect
from owner.models import Books
from django.views.generic import View,ListView,CreateView
from django.urls import reverse_lazy
from customer.forms import UserRegistrationForm,LoginForm,PasswordResetForm,OrderForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from customer.models import Cart,Orders
from customer.decorators import signin_required
from django.utils.decorators import method_decorator
from django.contrib import messages


# Create your views here.


@method_decorator(signin_required,name="dispatch")
class customerIndex(ListView):
    model = Books
    template_name = "cust_home.html"
    context_object_name = "books"

    # def get(self,request,*args,**kwargs):
    #     qs=Books.objects.all()
    #     return render(request,"cust_home.html",{"books":qs})

class SignUpView(CreateView):
    model = User
    template_name = "signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("signin")
    # def get(self,request,*args,**kwargs):
    #     form=UserRegistrationForm()
    #     return render(request,"signup.html",{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("signin")
    #     else:
    #         return render(request,"signup.html",{"form":form})


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

@signin_required
def signout(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

@method_decorator(signin_required,name="dispatch")
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


@signin_required
def add_to_cart(request,*args,**kwargs):
    book=Books.objects.get(id=kwargs["id"])
    user=request.user
    cart=Cart(product=book,
              user=user)
    cart.save()
    messages.success(request,"Item has been added to cart")
    return redirect("custhome")

@method_decorator(signin_required,name="dispatch")
class ViewMyCart(ListView):
    model = Cart
    template_name = "mycart.html"
    context_object_name = "carts"
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).exclude(status="cancelled").order_by("-date")


def remove_from_cart(request,*args,**kwargs):
    cart=Cart.objects.get(id=kwargs["id"])
    cart.status="cancelled"
    cart.save()
    messages.error(request,"Your item has been removed from cart")
    return redirect("custhome")

class OrderCreateView(CreateView):
    form_class = OrderForm
    template_name = "order_create.html"
    model = Orders
    def post(self,request,*args,**kwargs):
        cart_id=kwargs.get("c_id")
        product_id=kwargs.get("p_id")
        form=OrderForm(request.POST)
        if form.is_valid():
            order=form.save(commit=False)
            product=Books.objects.get(id=product_id)
            user=request.user
            order.product=product
            order.user=request.user
            order.save()
            cart=Cart.objects.get(id=cart_id)
            cart.status="orderplaced"
            cart.save()
            messages.success(request,"Your order has been placed")
        return redirect("custhome")
