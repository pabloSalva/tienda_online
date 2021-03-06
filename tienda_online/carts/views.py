from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart,CartProducts
from .utils import get_or_create_cart
from products.models import Product


def cart(request):
    
    cart = get_or_create_cart(request)    
    
    context = {
        'cart':cart
    }
    return render(request, 'carts/cart.html', context)


def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity',1)) #levanto la cantidad del form y por defecto le asigno 1
    
    cart_product = CartProducts.objects.create_or_update_quantity(cart=cart,
                                                                  product=product,
                                                                  quantity=quantity
                                                                )

    # cart.products.add(product, through_defaults={'quantity':quantity})
    context = {
        'cart_product': cart_product,
        'quantity': quantity,
        'product':product
    }   

    return render(request, 'carts/add.html',context)

def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    
    cart.products.remove(product)

    return redirect('carts:cart')

    
        


