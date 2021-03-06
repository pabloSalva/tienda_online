from django.db import models

from users.models import User


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    calle1 = models.CharField(max_length=200)
    calle2 = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    referencia = models.CharField(max_length=300)
    codigo_postal = models.CharField(max_length=10, null=False, blank=False)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo_postal

    def has_order(self):
        return self.order_set.count() >= 1     

    @property
    def address(self):
        return '{}-{}-{}'.format(self.ciudad, self.provincia, self.pais)    
    
    def update_default(self, default=False):
        self.default = default
        self.save()
