from django.urls import path
from .views import sceltagruppo, sceltalistino, sceltapagamento
from .views import misure_mancanti

app_name = 'ordini'

urlpatterns = [

    path('sceltaprogramma/<int:id>/',  sceltagruppo, name='scelta_gruppo'),
    path('sceltapagamento/<int:id>/',  sceltapagamento, name='scelta_pagamento'),
    path('sceltalistino/<int:id>/<int:pg>',
         sceltalistino, name='scelta_listino'),
    path('sceltalistino/',  misure_mancanti, name='misura_mancante'),
]
