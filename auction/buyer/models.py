from django.db import models
from seller.models import Product,SellerModel

# Create your models here.


class BuyerModel(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=6)
    
    def __str__(self):
        return self.name
    


class BuyerProfileModel(models.Model):
    buyer = models.OneToOneField(BuyerModel, related_name = 'buyer', on_delete=models.CASCADE,null = True)
    profile_pic = models.ImageField(upload_to='profile_pic/',null = True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def  __str__(self):
        return self.buyer.name
    
class BuyerCart(models.Model):
    buyer = models.ForeignKey(BuyerModel, related_name = 'buyercart', on_delete=models.CASCADE,null = True)
    product = models.ForeignKey(Product, related_name= 'cartproduct', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name
    
class Payment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='paid_products')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    
    def __str__(self):
        return f"  {self.product.name} - {self.buyer.name} - {self.amount}"   
    
class Order(models.Model):
    product = models.ForeignKey(Payment, related_name="orders", on_delete=models.CASCADE)
    seller = models.ForeignKey('seller.SellerModel', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )
    orderstatus = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')

    
    