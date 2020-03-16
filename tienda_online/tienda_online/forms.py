from django import forms

from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=50, required=True,
                                widget=forms.TextInput(attrs={
                                    'class' : 'form-control',
                                    'id' : 'username',
                                    'placeholder' : 'username'
                                }))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'class' : 'form-control',
                                 'id' : 'email',
                                 'placeholder'  : 'example@mail.com'
                             }))
    password = forms.CharField(min_length=8, max_length=50, required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class' : 'form-control',
                                    'id' : 'password',
                                }))
    password2 = forms.CharField(label='confirmar password',
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class' : 'form-control',
                                }))    
    #Funciones de validación de formularios para registro de usuario
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario se encuentra en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email') 

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El mail ya está en uso')
        return email

    def clean(self): #se usa sií necesito validar campos q dependan uno del otro, en este caso pass y pass2       
        cleaned_data = super().clean() #obtengo todos los campos del formulario ejecutando .clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2','Las contraseñas no coiciden')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )            