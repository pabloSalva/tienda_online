from django.shortcuts import render
from carts.utils import get_or_create_cart
from .utils import get_or_create_order, breadcrumb

from django.contrib.auth.decorators import login_required




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

