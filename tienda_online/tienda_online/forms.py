from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, max_length=50, required=True)
