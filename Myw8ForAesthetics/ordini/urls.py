from django.urls import path
from .views import sceltaprogramma, sceltalistino
from .views import misure_mancanti

app_name = 'ordini'

urlpatterns = [
    path('sceltaprogramma/<int:id>/',  sceltaprogramma, name='scelta_programma'),
    path('sceltalistino/<int:id>/',  sceltalistino, name='scelta_listino'),
    
    path('sceltalistino/',  misure_mancanti, name='misura_mancante'),
]
