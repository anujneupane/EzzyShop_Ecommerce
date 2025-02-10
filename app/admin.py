from django.contrib import admin
from .models import Customer,Product,Cart,OrderPlaced

# Register your models here.
@admin.register(Customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','province']

@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class cardAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class orderedAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status']

