import requests
import json
import datetime

from django.utils import timezone
from dateutil.parser import *

from django.conf import settings

from dateutil.parser import *
from django.utils.translation import gettext_lazy as _
import pdb


def autenticazione(request):

    s = requests.Session()
    s.auth = ('customercare', 'Nuova2507')
    indirizzoautenticazione = settings.GENERAL_WS_PATH + '/authenticate'
    response = s.get(indirizzoautenticazione)

    if response.status_code == 200:

        request.session['token'] = response.request.headers['Authorization']

    return response.json()


def dati_utente(request, mail):

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

        if utente['email'] == mail:

            pazienteid = utente['patient']['id']
            lingua = utente['preferred_lang']
            risposta = {'id': pazienteid, 'lingua': lingua}
            break

        else:

            risposta = {'id': False, 'lingua': False}

    return (risposta)


def dati_cliente_misure(request, mail):

    # entro superutente
    aut = autenticazione(request)
    datiutente = dati_utente(request, mail)
    if datiutente['id'] == False:
        return False
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


def dati_cliente_profilo(request, mail):

    # entro superutente
    aut = autenticazione(request)
    datiutente = dati_utente(request, mail)
    if datiutente['id'] == False:
        return False
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
    print(infopaziente['subscription_plans'])
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
                'programma_attuale': programma_attuale}

        return dati

    else:

        return False
