from django.urls import path
from .views import login_view, homepagecentro, logout_view, logout_auto_view

app_name = 'utente'

urlpatterns = [
    # Altre URL dell'applicazione...
    path('login/', login_view, name='login'),
    path('homepage/centro', homepagecentro, name='homec'),
    path('logout/', logout_view, name='logout'),
    path('logout_auto/', logout_auto_view, name='logout-auto'),
]
