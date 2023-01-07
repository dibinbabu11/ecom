from django.shortcuts import get_object_or_404, redirect, render
from django . http import HttpResponse
from ecomapp. models import product
from . models import Cart,Cartitem
from django. core.exceptions import ObjectDoesNotExist
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def add_cart(request,product_id):
    products=product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item=Cartitem.objects.get(product=products,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item=Cartitem.objects.create(product=products,quantity=1,cart=cart)
        cart_item.save()
    return redirect('cart:cart_detail')
def cart_deatil(request,total=0,counter=0,cart_item=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=Cartitem.objects.filter(cart=cart,active=True)
        for cartitem in cart_item:
            total += (cartitem.product.price * cartitem.quantity)
            counter += cartitem.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,"cart.html",{'cart_item':cart_item,'total':total,'counter':counter})

def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    products=get_object_or_404(product,id=product_id) 
    cart_item=Cartitem.objects.get(product=products,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item . save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')
def full_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    products=get_object_or_404(product,id=product_id) 
    cart_item=Cartitem.objects.get(product=products,cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
