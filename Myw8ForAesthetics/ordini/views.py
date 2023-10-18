from django.shortcuts import render, redirect
from django.conf import settings

from datetime import datetime

import requests
import pdb

from Myw8ForAesthetics.decorators import handle_exceptions, handle_error_response
from .form import FormRateale
# Create your views here.


@handle_exceptions
def sceltagruppo(request, id):
    # id è l'id del cliente
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

    # se il cliente non a il modulo lo deve compilare
    if cliente['compilazione_pcu'] == False:

        request.session['ultimo_utente'] = cliente
        return redirect('ordini:misura_mancante')
    else:
        request.session['cliente_ordine'] = cliente
        # richiamo il numero e il tipo di ordini effettuati
        url_backend = settings.BASE_URL + 'ordini/tipo_ordini/'+str(id)

        headers = {
            "Authorization": f"Token {request.session['auth_token']}"
        }
        response = requests.get(url_backend, headers=headers)

        if response.status_code == 200:
            tipo_ordine = response.json()
        elif response.status_code >= 400:
            return redirect('erroreserver', status_code=response.status_code, text=response.text)

        # caso nessun ordine inserito nel sistema per il cliente
        if tipo_ordine['ordini'] == 'nessuno':
            gruppi_visibili = 'primo_ordine'

        # caso un ordine small inserito nel sistema per il cliente
        elif tipo_ordine['ordini'] == 'solo_test':
            a = 0
        # caso un ordine non smal inserito nel sistema per il cliente
        elif tipo_ordine['ordini'] == 'completo':
            a = 0
        # caso piu ordini inseriti nel sistema per il cliente
        else:
            a = 0

        # se ha un beneficiario vado sui programmi kids
        if cliente['beneficiario_cognome']:
            minorenne = True
        else:
            minorenne = False

        request.session['cliente_ordine_eta'] = minorenne
        data = {
            'minorenne': minorenne,
            'gruppi_visibili': gruppi_visibili

        }

        url_backend = settings.BASE_URL + 'listini/gruppi/'
        headers = {"Authorization": f"Token {request.session['auth_token']}"}
        response = requests.get(url_backend, headers=headers, data=data)
        if response.status_code == 200:
            listini = response.json()
        elif response.status_code >= 400:
            return redirect('erroreserver', status_code=response.status_code, text=response.text)

        context = {'dati': listini, 'minore': minorenne}

        return render(request, 'ordini/scelta_gruppo.html', context)


@handle_exceptions
def sceltapagamento(request, id):
    # id è l'id del gruppo

    minore = request.session['cliente_ordine_eta']
    url_backend = settings.BASE_URL + 'listini/pagamenti/'+str(id)

    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        risposta = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    context = {'minore': minore, 'id': id, 'visibile':  risposta}

    return render(request, 'ordini/scelta_pagamento.html', context)


@handle_exceptions
def sceltalistino(request, id, pg):
    # id del gruppo
    # pg è una variabile per la modalita di pagamento

    url_backend = settings.BASE_URL + 'listini/sceltaprogrammi/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    minore = request.session['cliente_ordine_eta']
    if pg == 0:
        # pagamento unico
        pagamento = False
    else:
        pagamento = True
    params = {'minore': minore, 'id': id, 'pagamento': pagamento,
              'cliente_id': request.session['cliente_ordine']['id']}

    response = requests.get(url_backend, headers=headers, params=params)
    if response.status_code == 200:
        listini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    context = {'dati': listini, 'minore': minore}

    return render(request, 'ordini/scelta_programma.html', context)


@handle_exceptions
def riassuntoinfo(request, id):

    # recupero informazioni programma scelto
    url_backend = settings.BASE_URL + 'listini/programmi/' + str(id)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        programma = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    form = FormRateale()

    id_cliente = request.session['cliente_ordine']['id']
    if programma['programma_rateale']:
        rat = 1
    else:
        rat = 0

    context = {'programma': programma, 'form': form,
               'id_cliente': id_cliente, 'rat': rat}

    return render(request, 'ordini/riassunto_ordine.html', context)


def misure_mancanti(request):

    return render(request, 'ordini/misura_mancante.html')
