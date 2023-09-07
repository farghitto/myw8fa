from django.urls import path
from .views import sceltamenu, sceltacliente, sceltapostcliente, sceltamisure
from .views import get_codice_fiscale, search_clienti
from .views import crea_cliente, crea_cliente_piva, crea_cliente_minore
from .views import info_cliente
from .views import crea_misura

app_name = 'clienti'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('', sceltamenu, name='sceltamenu'),
    path('tipo', sceltacliente, name='tipocliente'),
    path('post', sceltapostcliente, name='postcliente'),
    path('misure',  sceltamisure, name='scelta_misure'),

    path('nuovo', crea_cliente, name='nuovocliente'),
    path('nuovopiva', crea_cliente_piva, name='nuovoclientepiva'),
    path('nuovominore', crea_cliente_minore, name='nuovoclienteminore'),

    path('nuovamisura', crea_misura, name='nuovamisura'),

    path('search/', search_clienti, name='search_clienti'),

    path('informazioni/<int:id>/', info_cliente, name='info_cliente'),



    path('ajax/cf', get_codice_fiscale, name='ajax_codice_fiscale')

]
