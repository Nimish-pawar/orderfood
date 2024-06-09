from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from product.models import ProductTable
from product.models import ProductTable, CartItem 
from product.models import ProductTable
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from product.models import Payment
import razorpay


def home(request):
    productData=ProductTable.objects.all()
    if request.method=="GET":
        st=request.GET.get('fooditam')
        if st!=None:
                productData=ProductTable.objects.filter(name__icontains=st)
    data = {
        'productData':productData
    }
    
    if request.user.is_authenticated:
        return render(request,"index.html",data)
    else:
        return redirect('/signin')
    


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:   
     if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return redirect('/signin')
     else:
        return render(request,"user/login.html")
    
    
def signout(request):
    logout(request)
    return redirect('/signin')

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        confpassword = request.POST["confirmpassword"]
        if password==confpassword:
            user=User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request,user)
            return redirect('/')
        else:
            return redirect('/signup')
    else:
        return render(request,"user/signup.html")



def add_to_cart(request, product_id):
    product = get_object_or_404(ProductTable, pk=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product=product, user=request.user, defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        # Handle anonymous user cart (using Django's session framework or a third-party library)
        pass

    # Redirect to cart view or display a success message
    return redirect('/')



def show_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.product.price * item.quantity for item in cart_items)
        grand_total = total 
        
        # Calculate the total price for each item
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
        
        context = {
            'cart_items': cart_items,
            'subtotal': total,
            'total': grand_total
        }

        return render(request, "pages/show_cart.html", context)

    else:
        return redirect('/signin')


def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        item = get_object_or_404(CartItem, id=item_id)

        if action == 'increment':
            item.quantity += 1
        elif action == 'decrement' and item.quantity > 1:
            item.quantity -= 1
        
        item.save()
    return redirect('show_cart')

def remove_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
    return redirect('show_cart')



def create_payment(request):
    if request.method == "POST":
        amount = int(request.POST['amount']) * 100  # Convert to paise
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        payment_obj = Payment(order_id=payment['id'], amount=amount / 100)
        payment_obj.save()
        return render(request, 'pages/payment_details.html', {'payment': payment, 'key_id': settings.RAZORPAY_KEY_ID})
    return render(request, 'pages/creat_payment.html')


def payment_detail(request, order_id):
    payment = Payment.objects.get(order_id=order_id)
    return render(request, 'pages/payment_detail.html', {'payment': payment, 'key_id': settings.RAZORPAY_KEY_ID})


def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature(data)
            payment = Payment.objects.get(order_id=data['razorpay_order_id'])
            payment.payment_id = data['razorpay_payment_id']
            payment.status = 'paid'
            payment.save()

            # Clear the user's cart after payment is successful
            if request.user.is_authenticated:
                CartItem.objects.filter(user=request.user).delete()

            # Redirect the user to the home page
            return redirect('/')
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'failure'})