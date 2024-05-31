from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import BuyerModel,BuyerProfileModel,BuyerCart,Payment,Order
from seller.models import Product,SellerModel
from public.views import Role
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import razorpay
from django.conf import settings
from razorpay.errors import BadRequestError
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.


def ind(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            br=BuyerModel.objects.get(email = email)
            pr=Product.objects.all()
        except:
            return redirect(BuyerLoginView)
        if br:
            username= br.name
        return render(request,'index.html',{'username':username,'pr':pr,'br':br})
    return render(request,'index.html')
        
    
def BuyerLoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        buyer = BuyerModel.objects.filter(email=email,password=password)
        if buyer:
            ur=BuyerModel()
            request.session['email'] = email
            request.session['id'] = ur.id
            return redirect(ind)
        else:
            return render(request, 'register.html')
    else:
        return render(request, 'login.html')

def BuyerRegisterView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            SellerModel.objects.get(email = email)
            messages.error(request, 'Email already exists')
            return redirect(BuyerRegisterView)
        except SellerModel.DoesNotExist:
            BuyerModel(name=name,email=email,phone=phone,password=password).save()
            return redirect(BuyerLoginView)
    else:
        return render(request,'register.html')


def BuyerProfileView(request):
    if 'email' in request.session:
        email = request.session['email']
        buyer = get_object_or_404(BuyerModel, email=email)
        
        # Access the related BuyerProfileModel directly
        buyer_profile, created = BuyerProfileModel.objects.get_or_create(buyer=buyer)
        print(buyer_profile)
        return render(request, 'profile.html', {'buyer_profile': buyer_profile, 'buyer': buyer})
        
    else:
        return redirect(BuyerLoginView)
    
def AddProfileView(request):
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
        
        

            buyer_model, created = BuyerModel.objects.get_or_create(email=email)

            buyer_profile, created = BuyerProfileModel.objects.get_or_create(buyer=buyer_model)
            buyer_profile.address = address
            buyer_profile.profile_pic = profile_pic
            buyer_profile.city = city
            buyer_profile.state = state
            buyer_profile.zipcode = zipcode
            buyer_profile.country = country
            buyer_profile.save()

            return redirect(ind) 
        return render(request, 'addprofile.html')
    return redirect(BuyerLoginView)


def EditProfileView(request):
    if 'email' in request.session:
        email = request.session['email']
        buyer_model = get_object_or_404(BuyerModel, email=email)
        buyer_profile, created = BuyerProfileModel.objects.get_or_create(buyer=buyer_model)

        if request.method == 'POST':
            # Retrieve form data directly from request.POST
            buyer_model.name = request.POST.get('name')
            buyer_model.phone = request.POST.get('phone')
            buyer_profile.address = request.POST.get('address')
            buyer_profile.city = request.POST.get('city')
            buyer_profile.state = request.POST.get('state')
            buyer_profile.zipcode = request.POST.get('zipcode')
            buyer_profile.country = request.POST.get('country')

            profile_pic = request.FILES.get('profile_pic')
            if profile_pic:
                buyer_profile.profile_pic = profile_pic

            # Save changes
            buyer_model.save()
            buyer_profile.save()

            return redirect(ind) 

        return render(request, 'editprofile.html', {'buyer_model': buyer_model, 'buyer_profile': buyer_profile})
    else:
        return redirect('buyer_login')

        
    
def BuyerLogOutView(request):
    request.session.flush()
    return redirect(to=Role)

def BuyerDeleteView(request):
    if 'email' in request.session:
        email = request.session['email']
        seller_model = get_object_or_404(BuyerModel, email=email)
        seller_model.delete()
        return redirect(BuyerRegisterView)
    else:
        return redirect(BuyerLoginView)
    
    
    
def ProductView(request):
    if 'email' in request.session:
        email = request.session['email']
        all_products = Product.objects.all()

        items_per_page = 1  

        paginator = Paginator(all_products, items_per_page)
        page = request.GET.get('page')

        try:
            ur = paginator.page(page)
        except PageNotAnInteger:
            
            ur = paginator.page(1)
        except EmptyPage:
           
            ur = paginator.page(paginator.num_pages)

        context = {'ur': ur}
        return render(request, 'display.html', context)

    
    return render(request, 'display.html')
    
def AddAuctionView(request,id):
    if 'email' in request.session:
        email = request.session['email']
        try:
            buyer = BuyerModel.objects.get(email=email)
            if request.method == 'POST':
                max_price_input = request.POST.get('max_price')
                product = Product.objects.get(id=id)
                if product:
                    if float(max_price_input) < float(product.min_price):
                        messages.error(request, 'The amount must be greater than the minimum bid price.')
                    elif product.max_price and float(max_price_input) <= float(product.max_price):
                        messages.error(request, 'The amount must be greater than the current bid amount.')
                    else:
                        product.max_price = max_price_input
                        product.winner = buyer
                        product.save()
                        messages.success(request, 'Auction bid submitted successfully.')
                        return redirect(ind)
            product = Product.objects.filter(winner=buyer).first()
            prd = Product.objects.filter(id=id)

            return render(request, 'addauction.html', {'product': product, 'prd': prd})
        except BuyerModel.DoesNotExist:
            return redirect(BuyerLoginView)
    else:
        return redirect(BuyerLoginView)
    
def AddToCartView(request, id):
    if 'email' in request.session:
        email = request.session['email']
        try:
            buyer = BuyerModel.objects.get(email=email)
            product = Product.objects.get(id=id)
            
            existing_cart_item = BuyerCart.objects.filter(buyer=buyer, product=product).first()

            if existing_cart_item:
                messages.info(request, 'Product is already in your cart.')
                return redirect(reverse('display-products'))
            else:
                cart_item = BuyerCart(buyer=buyer, product=product)
                cart_item.save()
                messages.success(request, 'Product added to cart successfully.')
            
                return redirect(ind) 
        except BuyerModel.DoesNotExist:
            return redirect(BuyerLoginView)
    else:
        return redirect(BuyerLoginView)
    
def DisplayCartView(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            buyer = BuyerModel.objects.get(email=email)
            products = Product.objects.filter(winner=buyer, is_closed=True)
            cart_items = BuyerCart.objects.filter(buyer=buyer)
            
            # Number of items per page for pagination
            items_per_page = 1  

            # Paginator for cart items
            paginator = Paginator(cart_items, items_per_page)
            page = request.GET.get('page')

            try:
                cart_items_paginated = paginator.page(page)
            except PageNotAnInteger:
                cart_items_paginated = paginator.page(1)
            except EmptyPage:
                cart_items_paginated = paginator.page(paginator.num_pages)

            context = {'cart_items': cart_items_paginated, 'products': products}
            return render(request, 'display_cart.html', context)
        except BuyerModel.DoesNotExist:
            return redirect(BuyerLoginView)
    else:
        return redirect(BuyerLoginView)
    
def DeleteCartView(request,id):
    if 'email' in request.session:
        email = request.session['email']
        try:
            BuyerModel.objects.get(email=email)
            cart_item = BuyerCart.objects.get(id=id)
            cart_item.delete()
            messages.success(request, 'Product removed from cart successfully.')
            return redirect(ind)
        except BuyerModel.DoesNotExist:
            return redirect(BuyerLoginView)
    else:
        return redirect(BuyerLoginView)
    
def ViewWinnerView(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            buyer = BuyerModel.objects.get(email=email)
            products = Product.objects.filter(winner=buyer, is_closed=True)
            context = {'products': products}
            return render(request, 'winner.html', context)
        except BuyerModel.DoesNotExist:
            return redirect(BuyerLoginView)
    return redirect(BuyerLoginView)

def get_wins_count(request):
    if 'email' in request.session:
        email = request.session['email']
        buyer = BuyerModel.objects.get(email=email)
        wins_count = Product.objects.filter(winner=buyer, is_closed=True).count()
        return JsonResponse({'wins_count': wins_count})
    return JsonResponse({'wins_count': 0})

def initiate_payment(request, product_id):
    if 'email' in request.session:
        email = request.session['email']
        print(email)
        product = get_object_or_404(Product, id=product_id)
        amount = int(product.max_price) * 100  # Convert amount to paise

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        order_id = payment_order['id']
        buyer = BuyerModel.objects.get(email = email)
        buyer_data = {'buyer': {
            'id': buyer.id,
            'name': buyer.name,
            'email': buyer.email,
            'phone' : buyer.phone,
            'password' : buyer.password
            # Add other fields as needed
        }}
            

        response_data = {'order_id': order_id, 'amount': amount}
        response_data.update(buyer_data)
        return JsonResponse(response_data, encoder=DjangoJSONEncoder)

    else:
        return redirect(BuyerLoginView)
    
@csrf_exempt
def confirm_payment(request, order_id, payment_id):
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    print(client)
    try:
        payment = client.payment.fetch(payment_id)
        print(payment)
        if payment['order_id'] == order_id and payment['status'] == 'captured':
            # Payment successful, update your models or perform other actions
            product_id = payment['notes'].get('product_id')
            product = get_object_or_404(Product, id=product_id)

            # Fetch the BuyerModel instance based on the email
            buyer_email = payment.get('email')
            if buyer_email:
                buyer = get_object_or_404(BuyerModel, email=buyer_email)

                # Create a Payment record in the database
                payment_obj = Payment(
                    buyer=buyer,
                    product=product,
                    amount=payment['amount'] / 100.0,
                )

                # Save the Payment object
                payment_obj.save()

                # Create an Order record in the database
                order = Order.objects.create(
                    product=payment_obj,
                    seller=product.seller,
                    orderstatus='Pending'  
                )

                product.is_paid = True
                product.save()

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failure', 'error': 'Buyer email not found'})
    except BadRequestError as e:
        print('Error:', str(e))

    return JsonResponse({'status': 'failure'})


def PaySuccess(request):
    return render(request, 'paymentsuccess.html')


def MyOrdersView(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            orders = Order.objects.filter(product__buyer__email=email)
            return render(request, 'myorder.html', {'orders': orders})
        except Order.DoesNotExist:
            return render(request, 'myorder.html', {'orders': []})
    return redirect('buyer_login')  # Adjust the URL name for your buyer login
            