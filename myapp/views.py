from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from myapp import cart_items
from .templatetags.cart import cart_total
MERCHANT_KEY = 'UNbhGZMaZmRcmt0L'

# Create your views here.



def index(request):
    product_object=Product.objects.all()
    webuser = User.objects.all()

    product_name=request.GET.get('product_name')
    if product_name != '' and product_name is not None:
        product_object=product_object.filter(title__icontains=product_name)

    # print('You are : ', request.session.get('email'))
    paginator=Paginator(product_object,8)
    page = request.GET.get('page')
    product_object=paginator.get_page(page)

    return render(request,'index.html',{'product_object':product_object, 'webuser':webuser})


def login(request):
    if request.POST:
        email=request.POST['email']
        password=request.POST['password']
        user = User.get_user_by_email(email)
        print(email, password)
        print(user)
        error_msg = None
        if user:
            if password == user.password:
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                return redirect('index')
            else:
                error_msg = 'Invalid Email or Password'
        else:
            error_msg = 'Invalid Email or Password'
        return render(request,'login.html',{'error':error_msg})
    return render(request,'login.html')


def signup(request):
    return render(request,'signup.html')


def registerUser(request):
    if request.POST:
        username=request.POST['username']
        email=request.POST['email']
        contact=request.POST['contact']
        password=request.POST['password']
        password2=request.POST['password2']

        value = {
            'username' : username,
            'email' : email,
            'contact' : contact
        }
        obj = User(username=username, email=email, contact=contact, password=password)

        error_msg = None
        if password != password2:
            # messages.error(request, 'Password did not match')
            error_msg = 'Password did not match!!'

        elif len(password) <= 6 and len(password2) <= 6:
            error_msg = 'Password must be of atleast 6 characters'
        elif len(contact) < 10:
            error_msg = 'Contact must be of atleast 10 digits'

        elif obj.exists():
            error_msg = 'Email already registered'


        if not error_msg:
            # obj.password = make_password(obj.password)
            obj.save()
            del error_msg
            return redirect('index')
        else:
            data = {
                'error': error_msg,
                'values' : value
            }
            return render(request,'signup.html', data)

    else:
        return render(request,'signup.html')


def readmore(request,id):
    product=Product.objects.get(id=id)
    return render(request,'readmore.html',{'product':product})


def checkout(request):
    product = Product.objects.all()
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        cart = request.session.get('cart')
        totalPrice11=request.POST['totalPrice11']
        products = Product.get_product_by_id(list(cart.keys()))

        for product in products:
            order = Order(name=name,email=email,address=address,city=city,state=state,zipcode=zipcode, product=product,
                      price=product.discount_price, quantity=cart.get(str(product.id)))
            id = order.order_id
            order.save()
            request.session['cart'] = {}


            param_dict = {
                'MID': 'zzPKFV24968141626954',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': totalPrice11,
                'CUST_ID': 'email',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
                }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict':param_dict})
    return render(request, 'checkout.html', {'product':product})


def logout(request):
    request.session.clear()
    return redirect('login')


def contact(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        print(name, email, message)
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        return  redirect('index')


def orders(request):
    user = request.session.get('user')
    order = Order.get_orders_by_user(user)
    print(order)
    return render(request,'order.html')


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

