from django.forms import ModelForm

from .models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'calle1', 'calle2', 'ciudad', 'provincia', 'pais', 'codigo_postal', 'referencia'
        ]

        labels = {
            'calle1':'Calle',
            'calle2':'Entre',
            'ciudad':'Ciudad',
            'provincia':'Provincia',
            'pais':'País',
            'codigo_postal':'Código postal',
            'referencia':'Referencia'
        }
    #para agregar atributos a los inputs modifico la funcion __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.fields['calle1'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'calle x #1234 '
        })
        self.fields['calle2'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Entre calle x y calle x1'
        })
        self.fields['ciudad'].widget.attrs.update({
            'class':'form-control'
        })
        self.fields['provincia'].widget.attrs.update({
            'class':'form-control'
        })
        self.fields['pais'].widget.attrs.update({
            'class':'form-control'
        })
        self.fields['codigo_postal'].widget.attrs.update({
            'class':'form-control'
        })
        self.fields['referencia'].widget.attrs.update({
            'class':'form-control'
        })    
    