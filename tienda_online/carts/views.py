from django.shortcuts import render
from .models import Cart

def cart(request):
    #compruebo que el usuario esté o no autenticado
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.get(cart_id=cart_id)
    else:
        cart = Cart.objects.create(user=user)#si el usuario es none tambien podrá crear un carrito y uuna session

    request.session['cart_id'] = cart.cart_id   #con esto ya generamos la session que almacena el id del carrito de compras 
    context = {}
    return render(request, 'carts/cart.html', context)


