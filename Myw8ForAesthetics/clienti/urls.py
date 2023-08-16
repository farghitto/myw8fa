from django.urls import path
from .views import sceltamenu, sceltacliente, ClienteView
from .views import ClienteView
from .views import get_codice_fiscale

app_name = 'clienti'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('', sceltamenu, name='sceltamenu'),
    path('tipo', sceltacliente, name='tipocliente'),
    path('nuovo', ClienteView.as_view(), name='nuovocliente'),
    
    
    path('ajax/cf', get_codice_fiscale, name='ajax_codice_fiscale')

]
