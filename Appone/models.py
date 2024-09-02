from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import CustomUserManager

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=35)
    mobile_number = models.CharField(unique=True,max_length=15)
    address = models.TextField(default=None,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile_number


class ProductInventory(models.Model):
    product_code = models.CharField(primary_key=True , max_length=20)
    product_name = models.CharField(max_length=60)
    product_image = models.FileField(upload_to='products', max_length=100,default=None)
    product_unit = models.CharField(max_length=30)
    product_category = models.CharField(max_length=50)
    qty = models.FloatField()
    cost = models.FloatField()
    selling_price = models.FloatField()
    first_purchase = models.DateField(auto_now=False, auto_now_add=False)
    last_purchase = models.DateField(auto_now=True)
    
    
class WebsiteOrder(models.Model):
    order_number = models.AutoField(primary_key=True)
    # product_id = models.ForeignKey("Appone.ProductInventory", on_delete=models.CASCADE)
    
    customer_name = models.CharField(max_length=50)
    customer_mobile_number = models.CharField(max_length=15)
    customer_address = models.TextField()
    payment_method = models.CharField(max_length=20)
    payment_id = models.CharField(max_length=50)
    is_paid = models.BooleanField()
    is_accepted = models.BooleanField()
    order_date = models.DateField(auto_now=True)
    bill_amount = models.FloatField()
    user_name = models.CharField(max_length=50)
    
    
class WebsiteOrderItems(models.Model):
    order_number = models.ForeignKey("Appone.WebsiteOrder", on_delete=models.CASCADE)
    product_code = models.ForeignKey("Appone.ProductInventory", on_delete=models.CASCADE)
    qty = models.IntegerField()
    product_price = models.FloatField()
    total_amount = models.FloatField()
    
    
    
class ContactUsForm(models.Model):
    customer_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15)
    subject = models.CharField(max_length=50)
    message = models.TextField() 
    is_resolved = models.BooleanField(default=False)   
