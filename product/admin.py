from django.contrib import admin
from product.models import ProductTable

# Register your models here.

class product(admin.ModelAdmin):
    list_display=('id','name','price','description','quantity','category','image')
    
admin.site.register(ProductTable, product)
    
