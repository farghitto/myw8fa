from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings

import requests


def ajaxCalcoloStato(request):

    bmi = request.GET.get('bmi')
    sesso = request.GET.get('sesso')

    data = {
        'bmi': bmi,
        'sesso': sesso

    }
    url_backend = settings.BASE_URL + 'cliente/api/stati_peso/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, data=data, headers=headers)
    if response.status_code == 200:
        stato_attuale = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    print(stato_attuale)
    return JsonResponse({"data": stato_attuale})
