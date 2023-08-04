from django.urls import path
from .views import login_view, homepagecentro

app_name = 'utente'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('login/', login_view, name='login'),
    path('homepage/centro', homepagecentro, name='homec'),
]
