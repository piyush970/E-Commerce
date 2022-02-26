from django.shortcuts import render
from django.views import View

from myapp.models import Product


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_product_by_id(ids)
        print(products,ids)
        return render(request,'cart.html',{'products':products})

