"""
URL configuration for orderfood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from orderfood.views import *
from orderfood import views 
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import show_cart, update_cart_item, remove_cart_item
from .views import create_payment, payment_detail, verify_payment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home),
    path('', views.home, name='home'),
    path('',home),
    path('signin/', signin),
    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('signout/', signout),
    path('signup/',signup),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', show_cart),
    path('cart/', show_cart, name='show_cart'),
    path('update/', update_cart_item, name='update_cart_item'),
    path('remove/', remove_cart_item, name='remove_cart_item'),
    path('create_payment/', create_payment, name='create_payment'),
    path('payment_detail/<str:order_id>/', payment_detail, name='payment_detail'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('show_cart/', show_cart, name='show_cart'),
    

    #path('' ,views.home),
    #path('signup/' ,views.signup),
    #path('login/' ,views.login),
]



if  settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)