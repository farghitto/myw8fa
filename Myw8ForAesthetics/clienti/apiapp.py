import requests
import json
import datetime
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
