from django.urls import path

from .views import inviosms,inviomail


app_name = 'amministrazione'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('mail/<str:testo>/', inviomail, name='inviomail'),
    path('sms', inviosms, name='inviosms'),
    
]
