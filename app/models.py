from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now 
PROVINCE_CHOICES = (
    ('Province 1','Province 1'),
    ('Province 2','Provice 2'),
    ('Bagmati','Bagmati'),
    ('Gandaki Pradesh','Gandaki Pradesh'),
    ('Karnali Pradesh','Karnali Pradesh'),
    ('Lumbini','Lumbini'),
    ('Sudhurpraschim Pradesh','Sudhurpraschim Pradesh'),
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    province = models.CharField(choices=PROVINCE_CHOICES, max_length=50)

    def _str_(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('E', 'Earings and Necklace'),
    ('S', 'Shoes'),
    ('M', 'Male'),
    ('F', 'Female'),
) 

class Product(models.Model):
    title = models.CharField(max_length=100)
    renting_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices = CATEGORY_CHOICES, max_length=2)
    materialandcare = models.TextField(null=True)
    product_image = models.ImageField(upload_to='producting')
    
    def _str_(self):
        return str(self.id)
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    rent_duration = models.CharField(max_length=6, default='4 days')

    def _str_(self):
        return str(self.id)


    @property
    def total_cost(self):
     return self.quantity * self.product.discounted_price        
    

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)



class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices =STATUS_CHOICES, default='Pending')      
    
       
    def _str_(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price  


RETURN_CHOICES = (
    ('Received','Received'),
    ('Fined','Fined'),
)
     
class ReturnOrder(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       quantity = models.PositiveIntegerField(default = 1)
       returned_date = models.DateTimeField(auto_now_add=True)
       status = models.CharField(max_length=50, choices = RETURN_CHOICES, default='Pending')


    