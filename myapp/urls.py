"""Ecomweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from .home import Index
from .cart_items import Cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(),name='index'),
    path('', Index.as_view(),name='index'),
    path('login', views.login,name='login'),
    path('signup', views.signup,name='signup'),
    path('registerUser', views.registerUser,name='registerUser'),
    path('<int:id>/', views.readmore,name='readmore'),
    path('checkout', views.checkout,name='checkout'),
    path('cart', Cart.as_view(),name='cart'),
    path('logout', views.logout,name='logout'),
    path('handlerequest/', views.handlerequest,name='handlerequest'),
    path('contact', views.contact,name='contact'),
    # path('orders', views.orders,name='orders'),
]
