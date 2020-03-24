from django.urls import path

from .views import ProductDetailView,ProductSearchListView

#genero esta variable para que en un futuro no existan choques entre rutas de igual nombre pero de  distita app
app_name = 'products'
#las rutas de esta app se escriben {%url 'products:name'%}

urlpatterns = [
    path('search', ProductSearchListView.as_view(), name='search'),
    path('<slug:slug>',ProductDetailView.as_view(), name='product' )
]
