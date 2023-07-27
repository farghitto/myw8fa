from django.urls import path
from .views import login_view

urlpatterns = [
    # Altre URL dell'applicazione...
    path('login/', login_view, name='login'),
]
