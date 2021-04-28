from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from.models import Category,Product
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.
def home(request):
    return HttpResponse("hello world")

def allProdCat(request,c_slug=None):
    c_page=None
    products_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        products_list=Product.objects.filter(category=c_page,available=True)
    else:
        products_list=Product.objects.all().filter(available=True)
    paginator=Paginator(products_list,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except (EmptyPage,InvalidPage):
        products=paginator.page(paginator.num_pages)

    return render(request,'category.html',{'category':c_page,'products':products})
def ProdCatDetail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})

def register(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        uname = request.POST["username"]
        email = request.POST["email"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]
        if pass1 == pass2:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "username already exist!!")
                return redirect('mycart:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already exist!!")
                return redirect('mycart:register')
            else:
                user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email,
                                                password=pass1)
                user.save();
                messages.info(request, "you are successfully registered here!!!")
                return redirect('mycart:register')
        else:
            messages.info(request, "password not matched")
            return redirect('mycart:register')
    else:
        return render(request, "registration.html")

def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/mycart')
        else:
            messages.info(request,"invalid credentials")
            return redirect('mycart:login')
    else:
        return render(request,"login.html")
def logout(request):
    auth.logout(request)
    return redirect('/mycart')