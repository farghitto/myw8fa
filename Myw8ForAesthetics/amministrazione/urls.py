from django.urls import path

from .views import inviosms, inviomailchiave, inviomailallegato


app_name = 'amministrazione'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('mail/<str:testo>/', inviomailchiave, name='inviomail'),
    path('sms', inviosms, name='inviosms'),
    path('mailallegato/<str:testo>/', inviomailallegato, name='inviomailallegato'),
]
