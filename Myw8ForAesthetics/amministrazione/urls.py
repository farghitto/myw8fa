from django.urls import path

from .views import inviosms, inviomailchiave, inviomailallegato
from .ajaxview import ajaxCalcoloStato


app_name = 'amministrazione'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('mail/<str:testo>/', inviomailchiave, name='inviomail'),
    path('sms', inviosms, name='inviosms'),
    path('mailallegato/<str:testo>/', inviomailallegato, name='inviomailallegato'),
    
    path('ajax/calcolo_stato', ajaxCalcoloStato, name='ajax_calcola_stato')
]
