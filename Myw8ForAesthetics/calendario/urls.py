from django.urls import path
from .views import appuntamenti, indice, aggiungi_appuntamento, rimuovi_appuntamento, modifica_appuntamento, conferma_appuntamento

app_name = 'calendario'


urlpatterns = [
    path('appuntamenti/', indice, name='appuntamenti'),
    path('listaappuntamenti/', appuntamenti, name='lista_appuntamenti'),
    path('add_event/', aggiungi_appuntamento
         , name='aggiungi_appuntamento'),
    path('remove_event/', rimuovi_appuntamento
         , name='rimuovi_appuntamento'),
    path('move_event/', modifica_appuntamento
         , name='modifica_appuntamento'),
    path('confirm_event/', conferma_appuntamento
         , name='conferma_appuntamento'),
    
    # Altre URL del tuo progetto Django...
]