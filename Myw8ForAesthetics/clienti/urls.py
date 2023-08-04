from django.urls import path
from .views import sceltamenu, sceltacliente

app_name = 'clienti'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('', sceltamenu, name='sceltamenu'),
    path('tipo', sceltacliente, name='tipocliente'),

]
