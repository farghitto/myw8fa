from django.urls import path
from .views import sceltagruppo, sceltalistino, sceltapagamento, riassuntoinfo
from .views import misure_mancanti, modulodati_mancante, moduloalimenti_mancante, invio_moduli
from .views import invio_ordine, elenco_ordini
from .views import info_ordine

app_name = 'ordini'

urlpatterns = [

    path('sceltaprogramma/<int:id>/',  sceltagruppo, name='scelta_gruppo'),
    path('sceltapagamento/<int:id>/',  sceltapagamento, name='scelta_pagamento'),
    path('sceltalistino/<int:id>/<int:pg>',
         sceltalistino, name='scelta_listino'),
    path('riassuntoprogramma/<int:id>/',
         riassuntoinfo, name='riassunto_programma'),
    path('sceltalistino/',  misure_mancanti, name='misura_mancante'),
    path('invioordine/<int:id>',  invio_ordine, name='invio_ordine_mail'),
    path('inviomoduli/<int:id>',  invio_moduli, name='invio_moduli_mail'),
    path('inserimentodati/<int:id>',  modulodati_mancante, name='modulodati_mancante'),
    path('inserimentoalimenti/<int:id>',  moduloalimenti_mancante, name='moduloalimenti_mancante'),
    path('lista_ordini/',  elenco_ordini, name='lista_ordini'),
    path('infoordine/<int:id>',  info_ordine, name='info_ordine'),
]
