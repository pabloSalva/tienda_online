from django.db import models

from django.contrib.auth.models import User

class Customer(User):
    class Meta: #utilizo esta clase para agregar funcionalidad al modelo User preestablecido
        proxy = True  

    def get_products(self):
        return ['producto1']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=20)
    biography = models.TextField(max_length=60)

   
    