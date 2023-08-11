from django.urls import path
from .views import sceltamenu, sceltacliente, ClienteView

app_name = 'clienti'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('', sceltamenu, name='sceltamenu'),
    path('tipo', sceltacliente, name='tipocliente'),
    path('nuovo', ClienteView.as_view(), name='nuovocliente'),

]
