from django.contrib import messages

from django.shortcuts import render, redirect, reverse, get_object_or_404

#esta función toma como argumento el nombre de una dirección y retorna la direccion misma
from django.urls import reverse_lazy

#Utilizo login_required para vistas basadas en funciones y LoginRequiredMixin para vistas basadas en clases
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#En clases utilizo SuccessMessageMixin para eviar mensajes de acción realizada con exito 
from django.contrib.messages.views import SuccessMessageMixin 

from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView



from .models import ShippingAddress
from .forms import ShippingAddressForm

class ShippingAddressListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user= self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Dirección Actualizada con éxito'

    #función para retornar a otra vista una vez actualizados los registros
    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')

    #utilizo la función dispatch de la clase LoginRequiredMixin la cual verifica el el usuario actual esté autenticado
    def dispatch(self,request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        
        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAddressDeleteView(LoginRequiredMixin,DeleteView):
    login_url = 'login'
    model = ShippingAddress
    template_name = "shipping_addresses/delete.html"
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        #Valido que ningún usuario malicioso pueda eliminar la dirección por default
        if self.get_object().default:
            return redirect('shipping_addresses:shipping_addresses')

        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)    

@login_required(login_url='login')    
def create(request):
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False) #guardo temporalmente la instancia hasta verificar el usuario
        shipping_address.user = request.user
        #si la dirección es la primera entonces la guardo como default
        shipping_address.default = not ShippingAddress.objects.filter(user=request.user).exists()
        shipping_address.save()

        messages.success(request, 'Direccion creada con éxito')
        return redirect('shipping_addresses:shipping_addresses')

    context = {
        'form':form
    }

    return render(request, 'shipping_addresses/create.html', context)


def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping_addresses')    