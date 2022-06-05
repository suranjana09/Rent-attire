from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from .models import Customer,Product, Cart, OrderPlaced, ReturnOrder
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, request
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import requests
from django.urls import reverse_lazy

class ProductView(View):
     def get(self,request):
         totalitem = 0
         earingsandnecklace = Product.objects.filter(category='E')
         shoes= Product.objects.filter(category='S')
         male = Product.objects.filter(category='M')
         female= Product.objects.filter(category='F')
         if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
         return render(request, 'app/home.html',{'earingsandnecklace':earingsandnecklace, 'shoes':shoes, 'male':male, 'female':female, 'totalitem':totalitem})

class ProductDetailView (DetailView, FormView):
     def get(self, request, pk):
         totalitem = 0
         product = Product.objects.get(pk=pk)
         item_already_in_cart= False
         if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
          item_already_in_cart= Cart.objects.filter(Q(product=product.id) & Q(user= request.user)).exists()
         return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

         

class SearchView(TemplateView):
     template_name = "app/search.html"
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
       # print(results)

        context["results"] = results
        return context
      


@login_required       
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id= product_id)
    if request.method =="POST":
        if request.POST.get('rent_duration'):
            savevalue = Cart()
            savevalue.rent_duration= request.POST.get('rent_duration')
            savevalue.save()
            return render(request,'app/productdetail.html')
    Cart(user=user, product = product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 100.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        #print(cart_product)
        if cart_product:  
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+=tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount,
                          'amount':amount, 'shipping_amount':shipping_amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/empty.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount



        data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount
        


        data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)  

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount
            


        data = {
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)              
        
@login_required   
def rent_now(request):
 return render(request, 'app/rentnow.html')

@login_required
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def earingsandnecklace(request):
    totalitem = 0
    earingsandnecklace = Product.objects.filter(category = 'E')
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/earingsandnecklace.html',{'earingsandnecklace':earingsandnecklace,'totalitem':totalitem})

def shoes(request):
    totalitem = 0
    shoes = Product.objects.filter(category = 'S')
    if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/shoes.html',{'shoes':shoes, 'totalitem':totalitem})

def malewear(request):
    totalitem = 0
    male = Product.objects.filter(category = 'M')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/malewear.html',{'male':male, 'totalitem':totalitem})

def femalewear(request):
    totalitem = 0
    female = Product.objects.filter(category = 'F')
    if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/femalewear.html',{'female':female, 'totalitem':totalitem}) 

class CustomerRegistrationView(View):
    def get(self, request):
     form = CustomerRegistrationForm()
     return render(request, 'app/customerregistration.html',
     {'form':form} )
    def post(self, request):
     form = CustomerRegistrationForm(request.POST)
     if form.is_valid():
         messages.success(request, 'Registered Successfully')
         form.save()
     return render(request, 'app/customerregistration.html',
     {'form':form} )   

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 100.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount
        totalamount = amount + shipping_amount    
    return render(request, 'app/checkout.html', {'add':add, 'totalamount' : totalamount,'cart_items':cart_items})



class KhaltiVerifyView(View):
    def get(self,request,*args, **kwargs):
        token = request.GET.get("token")
        amount = request.GET.get("amount")
        print(token, amount)
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
              "token": token,
              "amount": amount
        }
        headers = {
               "Authorization": "Key test_secret_key_d2fb9fad340b4255afc47d08f72e218a"
        }

        response = requests.post(url, payload, headers = headers)
        resp_dict = response.json()
        if resp_dict.get("idx"):
            success = True
        else:
            success = False    
        data ={
            "success": success

        }
        return JsonResponse(data)
        
    
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart= Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")    


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get (self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
          form = CustomerProfileForm(request.POST) 
          if form.is_valid():
              user = request.user
              name = form.cleaned_data['name'] 
              locality = form.cleaned_data['locality'] 
              city = form.cleaned_data['city'] 
              province = form.cleaned_data['province'] 
              reg = Customer(user=user, name=name, locality=locality, city=city, province=province)
              reg.save()
              messages.success(request, 'Congratulation!! Profile updated...')
          return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})    


