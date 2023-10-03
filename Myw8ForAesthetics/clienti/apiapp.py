import requests
import json
import datetime

from django.shortcuts import redirect

from django.utils import timezone
from dateutil.parser import *

from django.conf import settings

from dateutil.parser import *
from django.utils.translation import gettext_lazy as _
import pdb

# metodo per autenticazione dell'app


def autenticazione(request):

    s = requests.Session()
    s.auth = ('customercare', 'Nuova2507')
    indirizzoautenticazione = settings.GENERAL_WS_PATH + '/authenticate'
    response = s.get(indirizzoautenticazione)

    if response.status_code == 200:

        request.session['token'] = response.request.headers['Authorization']

    return response.json()

# metodo per trovare lid utente richiamando tutti gli utenti e confrontando il cellulare


def dati_utente(request, cellulare):

    # il token generato è preso dalla session
    token = request.session['token']
    s = requests.Session()
    # il token è inserito nel header della request
    s.headers.update({'Authorization': token})

    # creazione path
    indirizzopazienti = settings.GENERAL_WS_PATH + '/it/users/'
    response = s.get(indirizzopazienti)
    infoutente = response.json()
    # trovo attraverso la mail dall'utente il paziente sull'app

    for utente in infoutente:

        if utente['mobile'] == cellulare:

            pazienteid = utente['patient']['id']
            lingua = utente['preferred_lang']
            risposta = {'id': pazienteid, 'lingua': lingua}
            break

        else:

            risposta = {'id': False, 'lingua': False}

    return (risposta)


def dati_cliente_misure(request, cellulare, id_cliente, id_app, lingua_app):

    # entro superutente
    aut = autenticazione(request)
    if not id_app:
        datiutente = dati_utente(request, cellulare)
        if datiutente['id']:
            registradatiapp(request, id_cliente,
                            datiutente['id'], datiutente['lingua'])
        else:
            return False
    else:
        datiutente = {'id': id_app, 'lingua': lingua_app}
    # il token generato è preso dalla session
    token = request.session['token']
    s = requests.Session()
    # il token è inserito nel header della request
    s.headers.update({'Authorization': token})

    # trovo le misure inserite
    indirizzodati = settings.GENERAL_WS_PATH + '/' + \
        str(datiutente['lingua']) + '/' + "patients/" + \
        str(datiutente['id']) + '/' + 'measurements/'
    response = s.get(indirizzodati)
    infopaziente = response.json()
    datimisuradaritornare = []

    for misura in infopaziente:

        data = datetime.datetime.strptime(misura['date'], "%Y-%m-%dT%H:%M:%SZ")
        dato = {'data': data,
                'valore': misura['value'], 'misura': misura['measurementType']['name']}
        datimisuradaritornare.append(dato)

    return datimisuradaritornare


def dati_cliente_profilo(request, cellulare,  id_cliente, id_app, lingua_app):

    # entro superutente
    aut = autenticazione(request)
    if not id_app:
        datiutente = dati_utente(request, cellulare)
        if datiutente['id']:
            registradatiapp(request, id_cliente,
                            datiutente['id'], datiutente['lingua'])
        else:
            return False
    else:
        datiutente = {'id': id_app, 'lingua': lingua_app}
    # il token generato è preso dalla session
    token = request.session['token']
    s = requests.Session()
    # il token è inserito nel header della request
    s.headers.update({'Authorization': token})

    # trovo le informazoni richieste
    indirizzodati = settings.GENERAL_WS_PATH + '/' + \
        str(datiutente['lingua']) + '/' + "patients/" + str(datiutente['id'])
    response = s.get(indirizzodati)
    infopaziente = response.json()
    oggi = timezone.localdate()

    if infopaziente['subscription_plans']:
        for programma in infopaziente['subscription_plans']:

            data_da_confrontare = datetime.datetime.strptime(
                programma['end_validity'], "%Y-%m-%dT%H:%M:%SZ")

            # Estrai solo la parte della data (anno, mese e giorno)
            data_da_confrontare_date = data_da_confrontare.date()
            # Confronta le date
            if data_da_confrontare_date >= oggi:
                # La data da confrontare è prima della data di oggi

                data_scadenza = data_da_confrontare_date
                programma_attuale = programma['subscription_plan']['subscription']['description']
                break

            else:
                # La data da confrontare è dopo la data di oggi
                data_scadenza = 'Nessun programma attivo'
                programma_attuale = 'Nessun programma attivo'

        dati = {'data_scadenza': data_scadenza,
                'programma_attuale': programma_attuale,
                'data_creazione': infopaziente['user']['creation_date'],
                'peso_iniziale': infopaziente['initial_weight']
                }
        print(dati)
        return dati

    else:

        return False

# inserisci l'id dell'app nell'applicazione


def registradatiapp(request, id_cliente, id_app, lingua_app):

    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id_cliente)+'/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    dati = {
        'id_utente_app': id_app,
        'lingua_utente': lingua_app,
    }
    response = requests.patch(
        url_backend, data=dati, headers=headers)

    if response.status_code == 200:
        # Redirect alla lista dei clienti
        return True
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    return True
