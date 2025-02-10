from django.db import models
from django.contrib.auth.models import User

# Create your models here.
Province_choice =(
    ('Lumbini', 'Lumbini'),
    ('Bagmati', 'Bagmati'),
    ('Madhesh', 'Madhesh'),
    ('Koshi', 'Koshi'),
    ('Gandaki', 'Gandaki'),
    ('Sudurpashchim', 'Sudurpashchim'),
    ('Karnali', 'Karnali'),

)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    locality = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    zipcode = models.IntegerField()
    province = models.CharField(choices=Province_choice,max_length=70)

def __str__(self):
    return str(self.id)

category_choice = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)


class Product(models.Model):
    title = models.CharField(max_length=70)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField(max_length=200)
    brand = models.CharField(max_length=70)
    category = models.CharField( choices=category_choice,max_length=2)
    product_image = models.ImageField(upload_to = 'producting')
    
def __str__(self):
    return str(self.id)

class Cart(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.PositiveIntegerField(default = 1)

def __str__(self):
    return str(self.id)


status_choice = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'), 
    ('Cancel','Cancel'), 

)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer =models.ForeignKey(Customer, on_delete=models.CASCADE)
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default = 1)
    ordered_date = models.DateTimeField(auto_now_add= True)
    status = models.CharField(max_length=50,choices=status_choice, default = 'Pending')       

def __str__(self):
    return str(self.id)   

  

