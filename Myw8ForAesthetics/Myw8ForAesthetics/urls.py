"""
URL configuration for Myw8ForAesthetics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from utente.views import erroreserver

urlpatterns = [
    path('admin/', admin.site.urls),
    path('utente/', include('utente.urls')),
    path('cliente/', include('clienti.urls')),
    path('amministrazione/', include('amministrazione.urls')),
    path('ordini/', include('ordini.urls')),
    path('calendario/', include('calendario.urls')),
    


    path('erroreserver/<int:status_code>/<str:text>/',
         erroreserver, name='erroreserver'),

]
