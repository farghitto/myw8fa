from multiprocessing import context
from turtle import pd
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator

from datetime import datetime

import requests
import pdb

from Myw8ForAesthetics.decorators import handle_exceptions, handle_error_response
from amministrazione.views import inviomailchiave, inviosms, inviomailallegato, inviomailchiaveallegato
from .form import FormRateale
from clienti.form import FormChiave, ModuloInformazioniForm
from amministrazione.creapdfordini import moduloOrdine, moduloOrdineFirmato
# Create your views here.


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
            gruppi_visibili = 'ordine_proseguimento'
        # caso un ordine non smal inserito nel sistema per il cliente
        elif tipo_ordine['ordini'] == 'completo':
            gruppi_visibili = 'ordine_mantenimento'
        # caso piu ordini inseriti nel sistema per il cliente
        else:
            gruppi_visibili = 'ordine_mantenimento'

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


def riassuntoinfo(request, id):

    url_backend = settings.BASE_URL + 'listini/programmi/' + str(id)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        programma = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    id_cliente = request.session['cliente_ordine']['id']
    if programma['programma_rateale']:
        rat = 1
    else:
        rat = 0

    if request.method == 'POST':
        form = FormRateale(request.POST)

        if form.is_valid():

            url_backend = settings.BASE_URL + 'utente/utente/' + \
                str(request.session['user_id'])
            headers = {
                "Authorization": f"Token {request.session['auth_token']}"}
            response = requests.get(url_backend, headers=headers)
            if response.status_code == 200:
                utente = response.json()
            elif response.status_code >= 400:
                return redirect('erroreserver', status_code=response.status_code, text=response.text)

            dati = {
                'cliente': request.session['cliente_ordine']['id'],

                'consulente': utente['id'],
                'utente_inserimento': utente['id'],
                'ordine_confermato': False,
                'data_creazione': datetime.now(),
                'data_ultima_modifica': datetime.now(),
                'programma': programma['id'],
                'numero_rate': form.cleaned_data['rate'],
                'acconto': form.cleaned_data['acconto'],
                'data_ordine': form.cleaned_data['data_ordine']

            }

            # Effettua la richiesta POST all'API
            url_backend = settings.BASE_URL + 'ordini/ordini/'
            headers = {
                "Authorization": f"Token {request.session['auth_token']}"
            }
            response = requests.post(
                url_backend, data=dati, headers=headers)

            if response.status_code == 201:  # Status code per "Created"

                return redirect(reverse('ordini:invio_ordine_mail', args=[id_cliente]))
            elif response.status_code >= 400:
                return redirect('erroreserver', status_code=response.status_code, text=response.text)
        else:
            context = {'programma': programma, 'form': form,
                       'id_cliente': id_cliente, 'rat': rat}

            return render(request, 'ordini/riassunto_ordine.html', context)

    form = FormRateale()

    context = {'programma': programma, 'form': form,
               'id_cliente': id_cliente, 'rat': rat}

    return render(request, 'ordini/riassunto_ordine.html', context)


def misure_mancanti(request):

    return render(request, 'ordini/misura_mancante.html')


def invio_ordine(request, id):

    risposta = False
    if request.method == 'POST':

        azione = request.POST.get('azione')
        chiave = get_random_string(length=10, allowed_chars='0123456789')
        if azione == 'sms':
            risposta = inviosms(request, chiave, id)
            request.session['firma_moduli_ordine'] = chiave
            # Esegui l'invio SMS
        elif azione == 'email':
            # idemail invio ordine
            idemail = 1
            percorso = moduloOrdine(request, id)
            risposta = inviomailchiaveallegato(
                request, chiave, percorso, id, idemail)
            request.session['firma_moduli_ordine'] = chiave
            print(chiave)
            # Esegui l'invio Email
        elif azione == 'chiave':
            chiave_inserita = request.POST.get('chiave')
            chiave = request.session['firma_moduli_ordine']
            if chiave == chiave_inserita:
                # idemail invio ordine firmato
                idemail = 2
                percorso = moduloOrdineFirmato(request, id)
                risposta = inviomailallegato(request, percorso, id, idemail)
                # vedo se il cliente ha il modulo alimenti compilato
                url_backend = settings.BASE_URL + \
                    'cliente/clientedati/'+str(id)+'/'
                headers = {
                    "Authorization": f"Token {request.session['auth_token']}"}
                response = requests.get(url_backend, headers=headers)
                if response.status_code == 200:
                    risposta = response.json()
                elif response.status_code >= 400:
                    return redirect('erroreserver', status_code=response.status_code, text=response.text)

                if risposta['esiste']:
                    return render(request, 'ordini/email_successo.html')
                else:
                    return redirect('ordini:modulodati_mancante', id=id)

    form = FormChiave()
    context = {'id': id, 'inserimento': risposta, 'form': form}
    return render(request, 'ordini/invio.html', context)


def modulodati_mancante(request, id):

    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'

    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    form = ModuloInformazioniForm
    context = {'form': form}

    return render(request, 'ordini/moduloinfo.html', context)


def elenco_ordini(request):

    id_utente = request.session['user_id']
    url_backend = settings.BASE_URL + 'ordini/ordini_lista/' + str(id_utente)
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        ordini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # Imposta il numero di elementi da visualizzare per pagina
    paginator = Paginator(ordini, 8)  # 8 elementi per pagina
    # Ottieni il numero di pagina dalla query string
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'elementi': ordini,
    }

    # dataordine, cliente, programmaexit

    return render(request, 'ordini/lista_ordini.html', context)


def info_ordine(request, id):

    url_backend = settings.BASE_URL + 'ordini/ordine/' + str(id)
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        ordini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    context = {'ordini': ordini}
    
    return render(request, 'ordini/informazione_ordine.html', context)
