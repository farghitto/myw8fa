from django.urls import path
from .views import sceltaprogramma, sceltalistino

app_name = 'ordini'

urlpatterns = [
   path('sceltaprogramma',  sceltaprogramma, name='scelta_programma'),
   path('sceltalistino/<int:id>/',  sceltalistino, name='scelta_listino'),
]
