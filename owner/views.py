from django.shortcuts import render,redirect
from owner.forms import BookForm
from django.views.generic import View
from owner.models import Books


from django.http import HttpResponse

# Create your views here.

def admin_home(request): #function based view


    # return HttpResponse("<h1>Welcome Owner</h1>")
    return render(request,"admin_home.html")

# def add_book(request):
#     # return HttpResponse("<h1>Add New Books here</h1>")
#     return render(request,"add_book.html")

class AddBookView(View):
    def get(self,request):
        form=BookForm()
        return render(request,"add_book.html",{"form":form})

    def post(self,request):
        form=BookForm(request.POST,files=request.FILES)
        if form.is_valid():
            # print(form.cleaned_data.get("book_name"))
            # print(form.cleaned_data.get("author"))
            # print(form.cleaned_data.get("price"))
            # print(form.cleaned_data.get("copies"))
            #
            # qs=Books(book_name=form.cleaned_data.get("book_name"),
            #          author=form.cleaned_data.get("author"),
            #          amount=form.cleaned_data.get("price"),
            #          copies=form.cleaned_data.get("copies"))
            # qs.save()

            form.save()
            # return render(request,"add_book.html",{"msg":"book created"})
            return redirect("allbooks")
        else:
            return render(request,"add_book.html",{"form":form})

class BookListView(View):
    def get(self,request):
        qs=Books.objects.all()
        return render(request,"book_list.html",{"books":qs})

class BookDetailView(View):
    def get(self,request,*args,**kwargs):
        #kwargs={'id':3}
        qs=Books.objects.get(id=kwargs.get("id"))
        return render(request,"book_detail.html",{"book":qs})

class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        #kwargs={'id':1}
        qs=Books.objects.get(id=kwargs.get("id"))
        qs.delete()
        return redirect("allbooks")


class EditBookView(View):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.get(id=kwargs.get("id"))
        form=BookForm(instance=qs)
        return render(request,"book_edit.html",{"form":form})

    def post(self,request,*args,**kwargs):
        qs=Books.objects.get(id=kwargs.get("id"))
        form=BookForm(request.POST,instance=qs,files=request.FILES)
        if form.is_valid():
            qs.save()
        return redirect("allbooks")




def register(request):
    # return HttpResponse("<h1>Registration form</h1>")
     return render(request,"register.html")

def login(request):
    # return HttpResponse("<h1>Login Here</h1>")
     return render(request,"login.html")