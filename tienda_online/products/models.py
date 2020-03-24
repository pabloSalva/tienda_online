import uuid #libreria para generar ids aleatorios

from django.db import models
from django.utils.text import slugify

from django.db.models.signals import pre_save

class Product(models.Model):
    title =  models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    model = models.CharField(max_length= 20)
    image = models.ImageField(upload_to='products/',blank=False, null=False)
    slug = models.SlugField(unique=True, blank=False, null= False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    #método para generar slug automáticos
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

# función que genera slug a través de callback que cumple la misma función que el método save() de Product
def set_slug(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug: 
        
        slug = slugify(instance.title) #genera el slug a partir del título

        while Product.objects.filter(slug= slug).exists(): #si el titulo está repetido genero uno con id aleatorio

            slug = slugify('{}-{}'.format(instance.title,str(uuid.uuid4())[:8]))

        instance.slug = slug    
pre_save.connect(set_slug, sender=Product)    

