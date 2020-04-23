from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    def has_shipping_address(self):
        return self.shipping_address is not None


class Customer(User):
    #utilizo esta clase para agregar funcionalidad al modelo User preestablecido
    class Meta: 
        proxy = True  

    def get_products(self):
        return ['producto1']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=20)
    biography = models.TextField(max_length=60)

   
    