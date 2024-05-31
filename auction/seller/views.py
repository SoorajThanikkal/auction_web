from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Product
from public.views import Role
from buyer.models import BuyerProfileModel,BuyerModel,Order,Payment
from .forms import ProductForm,UpdateStatusForm 
from django.urls import reverse


        
def SellerRegister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            BuyerModel.objects.get(email = email)
            messages.error(request, 'Email already exists')
            return redirect(SellerRegister)
        except BuyerModel.DoesNotExist:
            SellerModel(name=name,email=email,phone=phone,password=password).save()
            return redirect(SellerLogin)
    else:
        return render(request,'sellerregister.html')
    
def SellerIndex(request):
    if 'email' in request.session:
        email = request.session['email']
        print(email)
        try:
            br=SellerModel.objects.get(email = email)
            pr = Product.objects.filter(seller = br)
            if br:
                username= br.name
                return render(request,'sellerindex.html',{'username':username,'pr':pr})
            else:
                return redirect(SellerRegister)
        except SellerModel.DoesNotExist:
            return redirect(SellerRegister)
    else:        
        return render(request,'sellerindex.html')

    
def SellerLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        seller = SellerModel.objects.filter(email=email,password=password)
        if seller:
            ur=SellerModel()
            request.session['email'] = email
            request.session['id'] = ur.id
            return redirect(SellerIndex)
        else:
            return render(request, 'sellerregister.html')
    else:
        return render(request, 'sellerlogin.html')
    
def SellerProfileView(request):
    if 'email' in request.session:
        email = request.session['email']
        seller = get_object_or_404(SellerModel, email=email)
        print(seller)
        seller_profile, created = SellerProfileModel.objects.get_or_create(seller=seller)
        print(seller_profile)
        return render(request, 'sellerprofile.html', {'seller_profile': seller_profile, 'seller': seller})
        
    else:
        return redirect(SellerLogin)
    
def AddSellerProfileView(request):
    if 'email' in request.session:
        email = request.session['email']
        print(email)
        
        if request.method == 'POST':
            address = request.POST.get('address')
            profile_pic = request.FILES.get('profile_pic')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            country = request.POST.get('country')
        
        

            seller_model, created = SellerModel.objects.get_or_create(email=email)

            seller_profile, created = SellerProfileModel.objects.get_or_create(seller=seller_model)
            print(created)
            seller_profile.address = address
            seller_profile.profile_pic = profile_pic
            seller_profile.city = city
            seller_profile.state = state
            seller_profile.zipcode = zipcode
            seller_profile.country = country
            seller_profile.save()

            return redirect(SellerIndex) 
        return render(request, 'addsellerprofile.html')
    return redirect(SellerLogin)

def EditSellerProfileView(request):
    if 'email' in request.session:
        email = request.session['email']
        seller_model = get_object_or_404(SellerModel, email=email)
        seller_profile, created = SellerProfileModel.objects.get_or_create(seller=seller_model)

        if request.method == 'POST':
            # Retrieve form data directly from request.POST
            seller_model.name = request.POST.get('name')
            seller_model.phone = request.POST.get('phone')
            seller_profile.address = request.POST.get('address')
            seller_profile.city = request.POST.get('city')
            seller_profile.state = request.POST.get('state')
            seller_profile.zipcode = request.POST.get('zipcode')
            seller_profile.country = request.POST.get('country')

            profile_pic = request.FILES.get('profile_pic')
            if profile_pic:
                seller_profile.profile_pic = profile_pic

            # Save changes
            seller_model.save()
            seller_profile.save()

            return redirect(SellerIndex) 

        return render(request, 'sellereditprofile.html', {'seller_model': seller_model, 'seller_profile': seller_profile})
    else:
        return redirect(SellerLogin)
    
        
def SellerLogOutView(request):
    request.session.flush()
    return redirect(Role)

def SellerDeleteView(request):
    if 'email' in request.session:
        email = request.session['email']
        seller_model = get_object_or_404(SellerModel, email=email)
        seller_model.delete()
        return redirect(SellerRegister)
    else:
        return redirect(SellerLogin)

def add_product(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            seller = SellerModel.objects.get(email=email)
            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.seller = seller
                    product.save()
                    messages.success(request, 'Auction added successfully.')
                    return redirect('product_list')  # Redirect to the product list page
            else:
                form = ProductForm()

            return render(request, 'addproducts.html', {'form': form})
        except SellerModel.DoesNotExist:
            return redirect(SellerRegister)
    return redirect(SellerLogin)


def product_list(request):
    if 'email' in request.session:
        email = request.session['email']
        sell = SellerModel.objects.get(email=email)

        # Retrieve products and their related orders
        products = Product.objects.filter(seller=sell)
        payment = Payment.objects.filter(product__seller=sell)
        print(payment)
        orders = Order.objects.filter(product__in=payment)

        return render(request, 'listproducts.html', {'products': products, 'orders': orders})
    else:
        return redirect(SellerLogin)

    
def BuyerContactView(request,id):
    if 'email' in request.session:
        email = request.session['email']
        try:
           buyer_profile = get_object_or_404(BuyerProfileModel, buyer__id=id)
           context = {'buyer_profile': buyer_profile}
           return render(request, 'contact.html', context)
        except BuyerProfileModel.DoesNotExist:
            return HttpResponse(status=404, message= 'Couldn\'t find')
    return redirect(SellerLogin)


def SingleProductView(request,id):
    if 'email' in request.session:
        email = request.session['email']
        try:
           product = get_object_or_404(Product, id=id)
           context = {'product': product}
           return render(request,'singleproduct.html', context)
        except Product.DoesNotExist:
            return HttpResponse(status=404, message= 'Couldn\'t find')
    return redirect(SellerLogin)

def ProductDeleteView(request, id):
    if 'email' in request.session:
        email = request.session['email']
        try:
            sell = SellerModel.objects.get(email=email)
            product = get_object_or_404(Product, id=id)
            product.delete()
            return redirect(SellerIndex)
        except SellerModel.DoesNotExist:
            return redirect(Role)
    else:
        return redirect(SellerLogin)
    
def CloseAuctionView(request, id):
    try:
        product = Product.objects.get(id=id, is_closed=False)
        highest_bidder = product.winner

        if highest_bidder:
            product.is_closed = True
            product.save()
            messages.success(request, f"Auction closed. Winner: {highest_bidder.name}")
        else:
            messages.warning(request, "No winner found. Auction cannot be closed.")
    except Product.DoesNotExist:
        messages.warning(request, "Auction not found or already closed.")

    url = reverse('product_list')
    return redirect(url)

def update_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = UpdateStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['new_status']
            order.orderstatus = new_status
            order.save()
            return redirect('product_list')  
    else:
        form = UpdateStatusForm()

    return render(request, 'update_status.html', {'order': order, 'form': form})

