from django.shortcuts import render,redirect
from .models import Product,Cart
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
import razorpay


# Create your views here.

def home(request):
    context={}
    data= Product.objects.all()
    context['data'] = data
    return render(request, 'index.html',context)

def product(request,id):
    context={}
    data= Product.objects.filter(id=id)
   
    context['data'] = data[0]
    return render(request, 'product.html',context)


def loginview(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('/')  # Replace 'home' with the name of your homepage URL
        else:
            messages.error(request, "Invalid email or password!")
    
    return render(request, 'login.html')

def cart(request):
    context={}
    data= Cart.objects.all()
    print('this is cart data',data)
    user=request.user
    cart=Cart.objects.filter(user=user.id)
    tb=0
    for i in cart:
        tb+=i.product.price*i.quantity
    context['data']=data
    context['tb']=tb
    
    return render(request, 'cart.html',context)

def addtocart(request,id):
    
    pid= Product.objects.get(id=id)
    user=request.user
   

        
    # Check if the product is already in the user's cart
    cart_item = Cart.objects.create(user=user, product=pid)
    cart_item.save()
    
    return redirect('/cart')

def signupview(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html')

        # Check if the user with this email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'signup.html')

        # Create user with hashed password
        user = User.objects.create_user(username=email, password=password, email=email)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('/login/')
    
    return render(request, 'signup.html')

def delete(request,id):
    cart = Cart.objects.filter(id = id)
    cart.delete()
    messages.success(request,'Pet removed from your cart!!')

    return redirect('/cart')

def logoutview(request):
    logout(request)
    return redirect('/login/')

def about(request):
    return render(request, 'about.html')
    

def makepayment(request):
    user= request.user
    cart= Cart.objects.filter(user=user.id)
    tb=0
    for i in cart:
        tb+=i.product.price* i.quantity
    
    client = razorpay.Client(auth=("rzp_test_jUMUt8q0Zgt1Jc", "ez3IEjbskPudiBZKob2LY7kN"))


    data = { "amount": tb*100, "currency": "INR", "receipt": "" }
    payment = client.order.create(data=data)
    context={'data':payment}

    return render(request,'pay.html',context)
