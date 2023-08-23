from django.urls import path
from .views import sceltamenu, sceltacliente, sceltapostcliente
from .views import ClienteView, ClientePivaView, ClienteMinoreView
from .views import get_codice_fiscale,search_clienti, crea_cliente

app_name = 'clienti'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('', sceltamenu, name='sceltamenu'),
    path('tipo', sceltacliente, name='tipocliente'),
    path('post', sceltapostcliente, name='postcliente'),
    
    path('nuovo', crea_cliente, name='nuovocliente'),
    path('nuovopiva', ClientePivaView.as_view(), name='nuovoclientepiva'),
    path('nuovominore', ClienteMinoreView.as_view(), name='nuovoclienteminore'),
    
    path('search/', search_clienti, name='search_clienti'),
    
    path('ajax/cf', get_codice_fiscale, name='ajax_codice_fiscale')

]
