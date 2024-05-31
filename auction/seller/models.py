from django.db import models


# Create your models here.
class SellerModel(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=6)
    
    def __str__(self):
        return self.name
    
class SellerProfileModel(models.Model):
    seller = models.OneToOneField(SellerModel, related_name = 'seller', on_delete=models.CASCADE,null = True)
    profile_pic = models.ImageField(upload_to='seller_profile_pic/',null = True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def  __str__(self):
        return self.seller.name
    
class Product(models.Model):
    seller = models.ForeignKey(SellerModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stock = models.IntegerField(null = True)
    pro_image = models.ImageField(upload_to='pro_image/',null=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2,null = True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    CATEGORY_CHOICES = (
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Furniture', 'Furniture'),
        ('Vehicle' , 'Vehicle' )
        
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    winner = models.ForeignKey('buyer.BuyerModel', on_delete=models.SET_NULL, null=True, blank=True, related_name='won_products')
    is_closed = models.BooleanField(default= False, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.name} - {self.seller.name}"
    
    
 


    