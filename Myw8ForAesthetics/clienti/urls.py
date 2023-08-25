from django.urls import path
from .views import sceltamenu, sceltacliente, sceltapostcliente
from .views import get_codice_fiscale,search_clienti
from .views import crea_cliente, crea_cliente_piva, crea_cliente_minore
from .views import info_cliente

app_name = 'clienti'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('', sceltamenu, name='sceltamenu'),
    path('tipo', sceltacliente, name='tipocliente'),
    path('post', sceltapostcliente, name='postcliente'),
    
    path('nuovo', crea_cliente, name='nuovocliente'),
    path('nuovopiva', crea_cliente_piva, name='nuovoclientepiva'),
    path('nuovominore', crea_cliente_minore, name='nuovoclienteminore'),
    
    path('search/', search_clienti, name='search_clienti'),
    
    path('informazioni/<int:id>/', info_cliente, name='info_cliente'),
    
    path('ajax/cf', get_codice_fiscale, name='ajax_codice_fiscale')

]
