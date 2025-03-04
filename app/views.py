from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views import View
from .models import Product, Customer,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,changepassword,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse  
from django.utils.decorators import method_decorator



class ProductView(View):
    def get(self, request):
        context = {
             'topwears': Product.objects.filter(category='TW'),
             'bottomwears': Product.objects.filter(category='BW'),
             'laptop': Product.objects.filter(category='L'),
             'mobile': Product.objects.filter(category='M')
         
            }
        return render(request, 'app/home.html',context)

class Product_detail_view(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product':product} )

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

def show_cart(request):
  user = request.user
  cart = Cart.objects.filter(user = user)
  amount = 0.0
  delivary_charge = 100.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user==user]

  if cart_product:
    for p in cart_product:
      temp = (p.quantity * p.product.discounted_price)
      amount += temp
    total_amount = amount + delivary_charge

    return render(request, 'app/showcarts.html',{'carts': cart,'total':total_amount,'amount':amount})
  
  else:
    return render(request, 'app/empty_cart.html')

def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']  
    c = Cart.objects.get(Q(product=prod_id) & Q(user =request.user))
    c.quantity +=1
    c.save()
    amount = 0.0
    delivary_charge = 100
    user = request.user
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      temp = (p.quantity * p.product.discounted_price)
      amount += temp
    total_amount = amount + delivary_charge

    data = {
      'quantity':c.quantity,
      'amount':amount,
      'total_amount': total_amount
    }

    return JsonResponse(data)


def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']  
    c = Cart.objects.get(Q(product=prod_id) & Q(user =request.user))
    c.quantity -=1
    c.save()
    amount = 0.0
    delivary_charge = 100
    user = request.user
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      temp = (p.quantity * p.product.discounted_price)
      amount += temp
    total_amount = amount + delivary_charge

    data = {
      'quantity':c.quantity,
      'amount':amount,
      'total_amount': total_amount
    }

    return JsonResponse(data)
  
def remove_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']  
      c = Cart.objects.filter(Q(product=prod_id) & Q(user =request.user))
      c.delete()
      amount = 0.0
      delivary_charge = 100
      user = request.user
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
        temp = (p.quantity * p.product.discounted_price)
        amount += temp
      total_amount = amount + delivary_charge

      data = {
      'amount':amount,
      'total_amount': total_amount
      }
      return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

def mobile(request,data = None):
  if data == None:
    mobiles = Product.objects.filter(category = 'M')
  elif data =='Oneplus' or data == 'Samsung' or data == 'Apple':
    mobiles = Product.objects.filter(category = 'M').filter(brand = data)
  return render (request, 'app/mobile.html', {'mobiles':mobiles})  
  
def laptop(request,data = None):
  if data == None:
    laptops = Product.objects.filter(category = 'L')
  elif data in ['Asus' , 'Predator' ,'Apple']:
    laptops = Product.objects.filter(category = 'L', brand = data)
  return render (request, 'app/laptop.html', {'laptops':laptops})  

def topwear(request,data = None):
  if data == None:
    topwears = Product.objects.filter(category = 'TW')
  elif data in ['Nike' , 'NorthFace' ,'Gucci']:
    topwears = Product.objects.filter(category = 'TW', brand = data)
  return render (request, 'app/topwear.html', {'topwears':topwears}) 

def bottomwear(request,data = None):
  if data == None:
    bottomwears = Product.objects.filter(category = 'BW')
  elif data in ['Nike' , 'Gucci' ,'Louis']:
    bottomwears = Product.objects.filter(category = 'BW', brand = data)
  return render (request, 'app/bottomwear.html', {'bottomwears': bottomwears}) 

class CustomerRegistration(View):
    def get(self,request):
       form = CustomerRegistrationForm()
       return render(request, 'app/customerregistration.html',{'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
          messages.success(request, 'Congratulations!! Registered Successfully')
          form.save()
        return render(request, 'app/customerregistration.html',{'form':form})  
    
def passchange(request):  
  if request.user.is_authenticated:
   if request.method == "POST":
      fm = changepassword(user=request.user,data=request.POST)
      if fm.is_valid():
         fm.save()
         update_session_auth_hash(request,fm.user)
         return HttpResponseRedirect('/changepassword/',messages.success(request,'Password Changed Successfully') )
   else:
      fm = changepassword(user=request.user)
   return render(request,'app/changepassword.html', {'form': fm})
  else:
     return HttpResponseRedirect('/login/')
  
@method_decorator(login_required,name='dispatch') ###for class based view method.decorator
class ProfileView(View):
  def get(self,request):
   form = CustomerProfileForm()
   return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
  
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
          profile = form.save(commit=False)
          profile.user = request.user
          profile.save()
          messages.success(request, 'Congratulations!! Customer Profile Saved Successfully')
          form.save()
    return render(request, 'app/profile.html',{'form':form,})


def address(request):
 address = Customer.objects.filter(user = request.user) 
 return render(request, 'app/address.html',{'add':address,'active':'btn-primary'})

def userlogout(request):
   logout(request)
   return redirect('login')

def checkout(request):
  user = request.user
  address = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  delivary_charge = 100
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
    for p in cart_product:
      temp = (p.quantity * p.product.discounted_price)
      amount += temp
    total_amount = amount + delivary_charge

  return render(request, 'app/checkout.html',{'address':address,'total_amount':total_amount,'cart_items':cart_items})

def paymentdone(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cartitm = Cart.objects.filter(user=user)
  for c in cartitm:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity =c.quantity).save()
    c.delete()
  return redirect('orders')  

def orders(request):
 order = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'op':order})





