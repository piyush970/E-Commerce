from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from .models import Product

class Index(View):
    def post(self, request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart items', request.session['cart'])
        return redirect('index')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        product_object = Product.objects.all()

        product_name = request.GET.get('product_name')
        if product_name != '' and product_name is not None:
            product_object = product_object.filter(title__icontains=product_name)
        print('You are : ', request.session.get('email'))

        paginator = Paginator(product_object, 8)
        page = request.GET.get('page')
        product_object = paginator.get_page(page)
        return render(request, 'index.html', {'product_object': product_object})