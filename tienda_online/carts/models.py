import uuid
import decimal
from django.db import models
from django.contrib.auth.models import User 
from products.models import Product

from django.db.models.signals import pre_save, post_save
from django.db.models.signals import m2m_changed


class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through='CartProducts')
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    FEE = 0.21

    def __str__(self):
        return self.cart_id

    def update_totals(self):
        self.update_subtotal()
        self.update_total()
        #me conecto con el modelo Order a través de la relación uno a muchos como sigue:
        if self.order:
            self.order.update_total()

    def update_subtotal(self):
        self.subtotal = sum([
            #calculo el subtotal de toda la lista de productos teniendo en cuenta la cantidad de cada producto
            cp.quantity * cp.product.price for cp in self.products_related()
         
         ])
        self.save()

    def update_total(self):
        self.total = self.subtotal +  (self.subtotal * decimal.Decimal(Cart.FEE)) 
        self.save()  

    #método para evitar el problema de n +1 query. utilizo el metodo select_related
    #esto obtiene todos los objetos CartProducts y Products en una sola linea de código.
    def products_related(self):
        return self.cartproducts_set.select_related('product')    


    #defino un property para centralizar la obtencion de una orden con respecto a un carrito
    @property
    def order(self):
        return self.order_set.first()




class CartProductManager(models.Manager):
    #método para extender al objeto objects en views.add()

    def create_or_update_quantity(self, cart, product, quantity=1):
        object, created = self.get_or_create(cart=cart, product=product)

        if not created:
            quantity = object.quantity + quantity

        object.update_quantity(quantity) 
        return object


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = CartProductManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()


#implemento un callback para asignar el cart_id

def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())  #si no hay un id lo genera a través de la clase uuid

pre_save.connect(set_cart_id,sender=Cart)


#callback para mantener el total del precio del carrito siempre actualizado

def update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

m2m_changed.connect(update_totals, sender=Cart.products.through)        

#callback para los objetos de tipo CartProducts 
def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.cart.update_totals()

post_save.connect(post_save_update_totals, sender = CartProducts)