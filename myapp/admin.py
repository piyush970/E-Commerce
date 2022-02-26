from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = "E-Commerce Administration"
admin.site.site_title = "E-Commerce"
admin.site.index_title = "Manage site"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','discount_price','price','category')
    search_fields = ('title','category',)
    list_editable = ('price','category',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','password')


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Contact)
