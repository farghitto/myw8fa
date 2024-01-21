from django.shortcuts import render
from django.http import JsonResponse

from django.conf import settings

import requests

import pdb


def appuntamenti(request):
    
    # Effettua la richiesta POST all'API
    url_backend = settings.BASE_URL + 'calendario/crea_appuntamento/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        appuntamenti = response.json()
    
    events = []

    for appuntamento in appuntamenti:
        events.append({
            'title': appuntamento['titolo'],
            'start': appuntamento['inizio'],
            'end': appuntamento['fine'],
            'id': appuntamento['id'],
            'descrizione': appuntamento['descrizione'],
        })
        
        print(events)
    return JsonResponse(events, safe=False)

def indice(request):  
    
    url_backend = settings.BASE_URL + 'calendario/crea_appuntamento/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        appuntamenti = response.json()
    context = {
        "events":appuntamenti,
    }
    return render(request,'calendario/calendario.html',context)
 

 
def aggiungi_appuntamento(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    description = request.GET.get("title", None)
    
    if end is None:
        end = start
    
    url_backend = settings.BASE_URL + 'calendario/crea_appuntamento/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    data = {
        'titolo' : title,
        'inizio' : start,
        'fine' : end,
        'descrizione' : description
         
    }
    
    
    response = requests.post(url_backend, data=data, headers=headers)
    if response.status_code == 200:
        appuntamenti = response.json()
    
    data = {}
    return JsonResponse(data)
 
# def update(request):
#     start = request.GET.get("start", None)
#     end = request.GET.get("end", None)
#     title = request.GET.get("title", None)
#     id = request.GET.get("id", None)
#     event = Events.objects.get(id=id)
#     event.start = start
#     event.end = end
#     event.name = title
#     event.save()
#     data = {}
#     return JsonResponse(data)
 
def rimuovi_appuntamento(request):
    id = request.GET.get("id", None)
    
    url_backend = settings.BASE_URL + 'calendario/elimina_appuntamento/' + str(id)
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    
    response = requests.delete(url_backend, headers=headers)
    data = {}
    return JsonResponse(data)