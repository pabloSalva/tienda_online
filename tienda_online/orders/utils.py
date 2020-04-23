from .models import Order
from django.urls import reverse


def get_or_create_order(cart,request):
    order = cart.order #utilizo el property
    # order = Order.objects.filter(cart=cart).first()

    if order is None and request.user.is_authenticated:
        
        order = Order.objects.create(cart = cart, user = request.user)

    if order:
        print(order.status)
        request.session['order_id'] = order.order_id  
        print(request.session['order_id'],order.order_id)  

    return order 

def breadcrumb(products=True, address=False, payment=False, confirmation=False):
    return [
        {'title':'Productos', 'active':products, 'url':reverse('orders:order')},
        {'title':'Dirección', 'active':address, 'url':reverse('orders:address')},
        {'title':'Pago', 'active':payment, 'url':reverse('orders:order')},
        {'title':'Confirmación', 'active':confirmation, 'url':reverse('orders:order')}, 
    ]