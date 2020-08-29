from django.shortcuts import render,redirect,get_object_or_404
from carts.utils import get_or_create_cart
from .utils import get_or_create_order, breadcrumb

from django.contrib.auth.decorators import login_required
 
from shipping_address.models import ShippingAddress




#permite restringir vistas para usuarios autenticados
@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    
    order = get_or_create_order(cart, request)
    print(order.order_id)
    context = {'order': order,
               'cart' : cart,
               'breadcrumb':breadcrumb()    
                }
    return render(request, 'orders/order.html', context)

@login_required(login_url = 'login')
def address(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    shipping_address = order.get_or_set_shipping_address()
    hay_opciones = request.user.shippingaddress_set.count() > 1

    context = {
        'cart':cart,
        'order':order,
        'shipping_address':shipping_address,
        'breadcrumb':breadcrumb(address=True),
        'hay_opciones':hay_opciones
    }

    return render(request, 'orders/address.html', context)


@login_required(login_url = 'login')
def select_address(request):
    shipping_addresses = request.user.shippingaddress_set.all()
    
    context = {
        'breadcrumb':breadcrumb(address=True),
        'shipping_addresses':shipping_addresses,
        
    }
    return render(request, 'orders/select_address.html',context)    
    
@login_required(login_url = 'login')
def check_address(request,pk):    
        cart = get_or_create_cart(request)
        order = get_or_create_order(cart, request)

        shipping_address = get_object_or_404(ShippingAddress, pk=pk)
        if request.user.id != shipping_address.user_id:
            return redirect('carts:cart')

        order.update_shipping_address(shipping_address)

        return redirect('orders:address')    
