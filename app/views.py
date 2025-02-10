from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views import View
from .models import Product, Customer,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,changepassword,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required


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

    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            Cart.objects.create(user=user, product=product)  
            messages.success(request, "Item added to cart successfully!")
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('cart')  # Redirect to the cart page


def buy_now(request):
 return render(request, 'app/buynow.html')





def orders(request):
 return render(request, 'app/orders.html')



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

 
def userlogout(request):
   logout(request)
   return redirect('login')

# # def checkout(request):
# #  return render(request, 'app/checkout.html')

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