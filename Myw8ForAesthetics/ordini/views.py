from django.shortcuts import render, redirect
from django.conf import settings

from datetime import datetime

import requests

from Myw8ForAesthetics.decorators import handle_exceptions, handle_error_response
# Create your views here.


@handle_exceptions
def sceltaprogramma(request, id):

    # chiamo per i dati del clienrte
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'

    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    request.session['cliente_ordine'] = cliente
    formato = "%Y-%m-%d"
    data_di_nascita = datetime.strptime(
        cliente['data_nascita'], formato)
    data_corrente = datetime.now()
    eta = data_corrente.year - data_di_nascita.year - \
        ((data_corrente.month, data_corrente.day) <
            (data_di_nascita.month, data_di_nascita.day))

    if eta < 18:
        minorenne = True
    else:
        minorenne = False
    request.session['cliente_ordine_eta'] = minorenne

    url_backend = settings.BASE_URL + 'listini/lista/' + str(minorenne)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        listini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    context = {'dati': listini, 'minore': minorenne}

    return render(request, 'ordini/scelta_gruppo.html', context)


@handle_exceptions
def sceltalistino(request, id):

    url_backend = settings.BASE_URL + 'listini/sceltaprogrammi/' + str(id)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        listini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    minore = request.session['cliente_ordine_eta']
    context = {'dati': listini, 'minore': minore}

    return render(request, 'ordini/scelta_programma.html', context)
