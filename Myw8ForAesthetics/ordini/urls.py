from django.urls import path
from .views import sceltaprogramma

app_name = 'ordini'

urlpatterns = [
   path('sceltaprogramma',  sceltaprogramma, name='scelta_programma'),

]
