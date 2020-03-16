from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

from .forms import RegisterForm

from django.contrib.auth.models import User

def index(request):

    context = {
       'message' : 'listado de productos',
       'title' : 'productos' ,
       'products' : [
            {
                'title' : 'camara bullet', 
                'price' : 100,
                'stock' : True
            },
            {
                'title' : 'cable utp-5e',
                'price' : 500,
                'stock' : True
            },
            {
                'title' : 'cable utp-6e',
                'price' : 800,
                'stock' : False
            }
       ]
    }
    return render(request, 'index.html', context) 

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            login(request,user)
            messages.success(request, 'bienvenide {}'.format(user.username))
            return redirect('index')     
        else: 
            messages.error(request, 'Usuario o constraseña invalidos')    

    return render(request, 'users/login.html',{

    })    

def logout_view(request):

    logout(request)
    messages.success(request, 'sesion cerrada con éxito')
    return redirect('login')    

def register(request):
    form = RegisterForm(request.POST or None) 

    if request.method == 'POST' and form.is_valid():
        

        user = form.save()

        if user: #Valido que el usuario se haya creado
            login(request, user)
            messages.success(request,'Usuario creado exitosamente')
            return redirect('index')
    
    context = {
        'form' : form ,
        'title': 'registro de usuarios'
    }
    return render(request, 'users/register.html',context)