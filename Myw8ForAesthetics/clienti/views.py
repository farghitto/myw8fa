import string
import json
import copy
import locale
import requests


from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string
from django.utils import timezone

from datetime import datetime

from codicefiscale import codicefiscale

from Myw8ForAesthetics.decorators import handle_exceptions, handle_error_response
from .models import Cliente
from .form import FormCliente, FormClientePiva, FormClienteMinore
from .form import FormMisure, FormMisureRiassunto
from .form import ClientiSearchForm, FormChiave
from .apiapp import dati_cliente_misure, dati_cliente_profilo
from amministrazione.creapdfcheckup import ModuloPersonal
from amministrazione.views import inviomailchiave, inviosms, inviomailallegato
from amministrazione.myofficeapi import crea_cliente_myoffice

import pdb


@handle_exceptions
def sceltacliente(request):

    return render(request, 'clienti/opzioniclienti.html')


@handle_exceptions
def sceltamenu(request):

    return render(request, 'clienti/sceltaregistrazione.html')


@handle_exceptions
def sceltapostcliente(request):

    return render(request, 'clienti/sceltadoporegistrazione.html')


@handle_exceptions
def sceltamisure(request):

    return render(request, 'clienti/sceltamisura.html')


@handle_exceptions
def sceltadopomisure(request):

    return render(request, 'clienti/sceltadopomisura.html')


@handle_exceptions
def get_codice_fiscale(request):

    cognome = request.GET.get('cognome')
    nome = request.GET.get('nome')
    sesso = request.GET.get('sesso')
    datanascita = request.GET.get('data')
    comune = request.GET.get('comune')

    try:
        cf = codicefiscale.encode(
            lastname=cognome,
            firstname=nome,
            gender=sesso,
            birthdate=datanascita,
            birthplace=comune,
        )

        data = {

            'message': 'Dati ottenuti con successo!',
            'content': cf
        }

    except:
        data = {

            'message': 'Errore!',
            'content': 'Errore!'
        }

    return JsonResponse(data)


@handle_exceptions
def crea_cliente(request):

    #
    if request.method == 'POST':
        form = FormCliente(request.POST)

        if form.is_valid():

            # Prendi i dati dal form
            dati = {
                'nome': form.cleaned_data['nome'],
                'cognome': form.cleaned_data['cognome'],
                'citta_nascita': form.cleaned_data['citta_nascita'],
                'provincia_nascita': form.cleaned_data['provincia_nascita'],
                'stato_nascita': form.cleaned_data['stato_nascita'],
                'data_nascita': form.cleaned_data['data_nascita'],
                'indirizzo': form.cleaned_data['indirizzo'],
                'cap': form.cleaned_data['cap'],
                'citta': form.cleaned_data['citta'],
                'provincia_residenza': form.cleaned_data['provincia_residenza'],
                'stato_residenza': form.cleaned_data['stato_residenza'],
                'codice_fiscale': form.cleaned_data['codice_fiscale'],
                'telefono': form.cleaned_data['telefono'],
                'cellulare': form.cleaned_data['cellulare'],
                'email': form.cleaned_data['email'],
                'sesso': form.cleaned_data['sesso'],
                'note': form.cleaned_data['note'],

            }

            # Effettua la richiesta POST all'API
            url_backend = settings.BASE_URL + 'cliente/lista/'
            headers = {
                "Authorization": f"Token {request.session['auth_token']}"
            }
            response = requests.post(
                url_backend, data=dati, headers=headers)

            if response.status_code == 201:  # Status code per "Created"
                # Redirect alla lista dei clienti o dove preferisci
                request.session['ultimo_utente'] = response.json()
                crea_cliente_myoffice(dati)
                return redirect('clienti:postcliente')
            elif response.status_code >= 400:
                return redirect('erroreserver', status_code=response.status_code, text=response.text)

    else:
        form = FormCliente()

    return render(request, 'clienti/nuovocliente.html', {'form': form})


@handle_exceptions
def crea_cliente_piva(request):

    #
    if request.method == 'POST':
        form = FormClientePiva(request.POST)

        if form.is_valid():

            # Prendi i dati dal form
            dati = {
                'nome': form.cleaned_data['nome'],
                'cognome': form.cleaned_data['cognome'],
                'citta_nascita': form.cleaned_data['citta_nascita'],
                'provincia_nascita': form.cleaned_data['provincia_nascita'],
                'stato_nascita': form.cleaned_data['stato_nascita'],
                'data_nascita': form.cleaned_data['data_nascita'],
                'indirizzo': form.cleaned_data['indirizzo'],
                'cap': form.cleaned_data['cap'],
                'citta': form.cleaned_data['citta'],
                'provincia_residenza': form.cleaned_data['provincia_residenza'],
                'stato_residenza': form.cleaned_data['stato_residenza'],
                'codice_fiscale': form.cleaned_data['codice_fiscale'],
                'telefono': form.cleaned_data['telefono'],
                'cellulare': form.cleaned_data['cellulare'],
                'email': form.cleaned_data['email'],
                'sesso': form.cleaned_data['sesso'],
                'note': form.cleaned_data['note'],
                'ragione_sociale': form.cleaned_data['ragione_sociale'],
                'sede': form.cleaned_data['sede'],
                'indirizzo_sede': form.cleaned_data['indirizzo_sede'],
                'cap_sede': form.cleaned_data['cap_sede'],
                'telefono_sede': form.cleaned_data['telefono_sede'],
                'email_sede': form.cleaned_data['email_sede'],
                'partita_iva': form.cleaned_data['partita_iva'],
                'codice_univoco': form.cleaned_data['codice_univoco'],

            }

            # Effettua la richiesta POST all'API
            url_backend = settings.BASE_URL + 'cliente/lista/'
            headers = {
                "Authorization": f"Token {request.session['auth_token']}"
            }
            response = requests.post(
                url_backend, data=dati, headers=headers)

            if response.status_code == 201:  # Status code per "Created"
                request.session['ultimo_utente'] = response.json()
                crea_cliente_myoffice(dati)
                return redirect('clienti:postcliente')
            elif response.status_code >= 400:
                return redirect('erroreserver', status_code=response.status_code, text=response.text)

    else:
        form = FormClientePiva()

    return render(request, 'clienti/nuovoclientepiva.html', {'form': form})


@handle_exceptions
def crea_cliente_minore(request):

    #
    if request.method == 'POST':
        form = FormClienteMinore(request.POST)

        if form.is_valid():

            # Prendi i dati dal form
            dati = {
                'nome': form.cleaned_data['nome'],
                'cognome': form.cleaned_data['cognome'],
                'citta_nascita': form.cleaned_data['citta_nascita'],
                'provincia_nascita': form.cleaned_data['provincia_nascita'],
                'stato_nascita': form.cleaned_data['stato_nascita'],
                'data_nascita': form.cleaned_data['data_nascita'],
                'indirizzo': form.cleaned_data['indirizzo'],
                'cap': form.cleaned_data['cap'],
                'citta': form.cleaned_data['citta'],
                'provincia_residenza': form.cleaned_data['provincia_residenza'],
                'stato_residenza': form.cleaned_data['stato_residenza'],
                'codice_fiscale': form.cleaned_data['codice_fiscale'],
                'telefono': form.cleaned_data['telefono'],
                'cellulare': form.cleaned_data['cellulare'],
                'email': form.cleaned_data['email'],
                'sesso': form.cleaned_data['sesso'],
                'note': form.cleaned_data['note'],
                'beneficiario_nome': form.cleaned_data['beneficiario_nome'],
                'beneficiario_cognome': form.cleaned_data['beneficiario_cognome'],
                'beneficiario_codice_fiscale': form.cleaned_data['beneficiario_codice_fiscale'],
                'beneficiario_cellulare': form.cleaned_data['beneficiario_cellulare'],

            }

            # Effettua la richiesta POST all'API
            url_backend = settings.BASE_URL + 'cliente/lista/'
            headers = {
                "Authorization": f"Token {request.session['auth_token']}"
            }
            response = requests.post(
                url_backend, data=dati, headers=headers)

            if response.status_code == 201:  # Status code per "Created"
                request.session['ultimo_utente'] = response.json()
                crea_cliente_myoffice(dati)
                return redirect('clienti:postcliente')
            elif response.status_code >= 400:
                return redirect('erroreserver', status_code=response.status_code, text=response.text)

    else:
        form = FormClienteMinore()

    return render(request, 'clienti/nuovoclienteminore.html', {'form': form})


@handle_exceptions
def search_clienti(request):

    form = ClientiSearchForm(request.GET)
    url_backend = settings.BASE_URL + 'cliente/lista'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        clienti = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    if form.is_valid():

        search_query = form.cleaned_data['search_query']
        elementi = [cliente for cliente in clienti if cliente['cognome'].lower(
        ).startswith(search_query.lower())]

    else:

        elementi = clienti

    # Imposta il numero di elementi da visualizzare per pagina
    paginator = Paginator(elementi, 8)  # 8 elementi per pagina
    # Ottieni il numero di pagina dalla query string
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'elementi': elementi,
        'form': form
    }

    return render(request, 'clienti/elencoclienti.html', context)


def info_cliente(request, id):

    # per la lingua delle date
    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
    # prendo l'url il token chiamoil server per il cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'

    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        clienti = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    # prendo il peso iniziale dal server per il cliente
    url_backend = settings.BASE_URL + 'cliente/peso/'+str(id)+'/'

    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        peso = response.json()

    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    # partita iva
    if clienti['ragione_sociale']:

        form = FormClientePiva(initial=clienti)
        for field in form:
            field.field.widget.attrs['disabled'] = 'disabled'

        dati_app = dati_cliente_profilo(
            request, clienti['cellulare'], clienti['id'], clienti['id_utente_app'], clienti['lingua_utente'])
        if dati_app:
            oggi = timezone.localdate()
            differenza_data = dati_app['data_scadenza'] - oggi
            numero_giorni = differenza_data.days
            programma = dati_app['programma_attuale']
            scadenza = dati_app['data_scadenza'].strftime("%d %B, %Y")
        else:
            programma = 'Non disponibile'
            scadenza = 'Non disponibile'
            numero_giorni = 'Non disponibile'

        data_is = datetime.strptime(
            clienti['data_creazione'][0:10], "%Y-%m-%d")
        data_da_confrontare_date = data_is.date()
        data_creazione = data_da_confrontare_date.strftime("%d %B, %Y")

        peso_desiderato = str(clienti['peso_desiderato'])
        if peso_desiderato is None or peso_desiderato == 'None':
            peso_desiderato = 'Non disponibile'

        context = {
            'form': form, 'id': clienti['id'], 'programma': programma,
            'data_creazione': data_creazione, 'giorni': numero_giorni,
            'data_scadenza': scadenza,
            'peso_desiderato': peso_desiderato, 'peso_iniziale': peso['peso']
        }

        return render(request, 'clienti/infoclientepiva.html',  context)
    # minore
    elif clienti['beneficiario_cognome']:

        form = FormClienteMinore(initial=clienti)
        for field in form:
            field.field.widget.attrs['disabled'] = 'disabled'

        dati_app = dati_cliente_profilo(
            request, clienti['cellulare'], clienti['id'], clienti['id_utente_app'], clienti['lingua_utente'])
        if dati_app:
            oggi = timezone.localdate()
            differenza_data = dati_app['data_scadenza'] - oggi
            numero_giorni = differenza_data.days
            programma = dati_app['programma_attuale']
            scadenza = dati_app['data_scadenza'].strftime("%d %B, %Y")
        else:
            programma = 'Non disponibile'
            scadenza = 'Non disponibile'
            numero_giorni = 'Non disponibile'

        data_is = datetime.strptime(
            clienti['data_creazione'][0:10], "%Y-%m-%d")
        data_da_confrontare_date = data_is.date()
        data_creazione = data_da_confrontare_date.strftime("%d %B, %Y")

        peso_desiderato = clienti['peso_desiderato']
        if peso_desiderato is None:
            peso_desiderato = 'Non disponibile'

        context = {
            'form': form, 'id': clienti['id'], 'programma': programma,
            'data_creazione': data_creazione, 'giorni': numero_giorni,
            'data_scadenza': scadenza,
            'peso_desiderato': peso_desiderato, 'peso_iniziale': peso['peso']
        }

        return render(request, 'clienti/infoclienteminore.html', context)
    # altri
    else:
        form = FormCliente(initial=clienti)
        for field in form:
            field.field.widget.attrs['disabled'] = 'disabled'

        dati_app = dati_cliente_profilo(
            request, clienti['cellulare'], clienti['id'], clienti['id_utente_app'], clienti['lingua_utente'])
        if dati_app:
            oggi = timezone.localdate()
            differenza_data = dati_app['data_scadenza'] - oggi
            numero_giorni = differenza_data.days
            programma = dati_app['programma_attuale']
            scadenza = dati_app['data_scadenza'].strftime("%d %B, %Y")
            data_c = datetime.strptime(
                dati_app['data_creazione'][0:10], "%Y-%m-%d")
            data_da_confrontare_date = data_c.date()
            data_creazione = data_da_confrontare_date.strftime("%d %B, %Y")

            peso_iniziale = dati_app['peso_iniziale']

        else:
            programma = 'Non disponibile'
            scadenza = 'Non disponibile'
            numero_giorni = 'Non disponibile'
            data_creazione = 'Non disponibile'
            peso_iniziale = 'Non disponibile'

        peso_desiderato = clienti['peso_desiderato']
        if peso_desiderato is None:
            peso_desiderato = 'Non disponibile'

        context = {
            'form': form, 'id': clienti['id'], 'programma': programma,
            'data_creazione': data_creazione, 'giorni': numero_giorni,
            'data_scadenza': scadenza,
            'peso_desiderato': peso_desiderato, 'peso_iniziale': peso_iniziale
        }

        return render(request, 'clienti/infocliente.html',  context)


@handle_exceptions
def modifica_cliente(request, id):

    # prendo l'url il token chiamo il server per il cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'

    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }

    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        clienti = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    # partita iva
    if clienti['ragione_sociale']:

        if request.method == 'POST':

            form = FormClientePiva(request.POST)

            if form.is_valid():

                # Prendi i dati dal form
                payload = {
                    'nome': form.cleaned_data['nome'],
                    'cognome': form.cleaned_data['cognome'],
                    'citta_nascita': form.cleaned_data['citta_nascita'],
                    'provincia_nascita': form.cleaned_data['provincia_nascita'],
                    'stato_nascita': form.cleaned_data['stato_nascita'],
                    'data_nascita': form.cleaned_data['data_nascita'],
                    'indirizzo': form.cleaned_data['indirizzo'],
                    'cap': form.cleaned_data['cap'],
                    'citta': form.cleaned_data['citta'],
                    'provincia_residenza': form.cleaned_data['provincia_residenza'],
                    'stato_residenza': form.cleaned_data['stato_residenza'],
                    'codice_fiscale': form.cleaned_data['codice_fiscale'],
                    'telefono': form.cleaned_data['telefono'],
                    'cellulare': form.cleaned_data['cellulare'],
                    'email': form.cleaned_data['email'],
                    'sesso': form.cleaned_data['sesso'],
                    'note': form.cleaned_data['note'],
                    'ragione_sociale': form.cleaned_data['ragione_sociale'],
                    'sede': form.cleaned_data['sede'],
                    'indirizzo_sede': form.cleaned_data['indirizzo_sede'],
                    'cap_sede': form.cleaned_data['cap_sede'],
                    'telefono_sede': form.cleaned_data['telefono_sede'],
                    'email_sede': form.cleaned_data['email_sede'],
                    'partita_iva': form.cleaned_data['partita_iva'],
                    'codice_univoco': form.cleaned_data['codice_univoco'],
                }

                # Effettua la richiesta Put all'API per aggiornare

                response = requests.put(
                    url_backend, data=payload, headers=headers)

                if response.status_code == 200:
                    # Redirect alla lista dei clienti
                    return redirect('clienti:search_clienti')
                elif response.status_code >= 400:
                    return redirect('erroreserver', status_code=response.status_code, text=response.text)
                # creare una pagina server error

            else:
                return render(request, 'clienti/modificaclientepiva.html',  {'form': form})

        else:
            form = FormClientePiva(initial=clienti)
            return render(request, 'clienti/modificaclientepiva.html',  {'form': form})
    # minore
    elif clienti['beneficiario_cognome']:

        if request.method == 'POST':

            form = FormClienteMinore(request.POST)

            if form.is_valid():

                # Prendi i dati dal form
                payload = {
                    'nome': form.cleaned_data['nome'],
                    'cognome': form.cleaned_data['cognome'],
                    'citta_nascita': form.cleaned_data['citta_nascita'],
                    'provincia_nascita': form.cleaned_data['provincia_nascita'],
                    'stato_nascita': form.cleaned_data['stato_nascita'],
                    'data_nascita': form.cleaned_data['data_nascita'],
                    'indirizzo': form.cleaned_data['indirizzo'],
                    'cap': form.cleaned_data['cap'],
                    'citta': form.cleaned_data['citta'],
                    'provincia_residenza': form.cleaned_data['provincia_residenza'],
                    'stato_residenza': form.cleaned_data['stato_residenza'],
                    'codice_fiscale': form.cleaned_data['codice_fiscale'],
                    'telefono': form.cleaned_data['telefono'],
                    'cellulare': form.cleaned_data['cellulare'],
                    'email': form.cleaned_data['email'],
                    'sesso': form.cleaned_data['sesso'],
                    'note': form.cleaned_data['note'],
                    'beneficiario_nome': form.cleaned_data['beneficiario_nome'],
                    'beneficiario_cognome': form.cleaned_data['beneficiario_cognome'],
                    'beneficiario_codice_fiscale': form.cleaned_data['beneficiario_codice_fiscale'],
                    'beneficiario_cellulare': form.cleaned_data['beneficiario_cellulare'],
                }

                # Effettua la richiesta Put all'API per aggiornare

                response = requests.put(
                    url_backend, data=payload, headers=headers)

                if response.status_code == 200:

                    # Redirect alla lista dei clienti
                    return redirect('clienti:search_clienti')
                elif response.status_code >= 400:
                    return redirect('erroreserver', status_code=response.status_code, text=response.text)
                # creare una pagina server error

            else:
                return render(request, 'clienti/modificaclienteminore.html',  {'form': form})

        else:
            form = FormClienteMinore(initial=clienti)
            return render(request, 'clienti/modificaclienteminore.html',  {'form': form})
    # altri
    else:

        if request.method == 'POST':

            form = FormCliente(request.POST)

            if form.is_valid():

                # Prendi i dati dal form
                misure = {
                    'nome': form.cleaned_data['nome'],
                    'cognome': form.cleaned_data['cognome'],
                    'citta_nascita': form.cleaned_data['citta_nascita'],
                    'provincia_nascita': form.cleaned_data['provincia_nascita'],
                    'stato_nascita': form.cleaned_data['stato_nascita'],
                    'data_nascita': form.cleaned_data['data_nascita'],
                    'indirizzo': form.cleaned_data['indirizzo'],
                    'cap': form.cleaned_data['cap'],
                    'citta': form.cleaned_data['citta'],
                    'provincia_residenza': form.cleaned_data['provincia_residenza'],
                    'stato_residenza': form.cleaned_data['stato_residenza'],
                    'codice_fiscale': form.cleaned_data['codice_fiscale'],
                    'telefono': form.cleaned_data['telefono'],
                    'cellulare': form.cleaned_data['cellulare'],
                    'email': form.cleaned_data['email'],
                    'sesso': form.cleaned_data['sesso'],
                    'note': form.cleaned_data['note'],
                }

                # Effettua la richiesta Put all'API per aggiornare

                response = requests.put(
                    url_backend, data=misure, headers=headers)

                if response.status_code == 200:

                    # Redirect alla lista dei clienti
                    return redirect('clienti:search_clienti')
                elif response.status_code >= 400:
                    return redirect('erroreserver', status_code=response.status_code, text=response.text)

            else:
                return render(request, 'clienti/modificacliente.html',  {'form': form})

        else:
            form = FormCliente(initial=clienti)
            return render(request, 'clienti/modificacliente.html',  {'form': form})


@handle_exceptions
def crea_misura(request):

    dati_cliente = request.session['ultimo_utente']
    if request.method == 'POST':
        form = FormMisure(request.POST)

        if form.is_valid():

            # Prendi i dati dal form
            misure = {
                'cliente': str(dati_cliente['id']),
                'peso': form.cleaned_data['peso'],
                'altezza': form.cleaned_data['altezza'],
                'bmi': form.cleaned_data['bmi'],
                'grasso_corporeo': form.cleaned_data['grasso_corporeo'],
                'muscolatura': form.cleaned_data['muscolatura'],
                'metabolismo': form.cleaned_data['metabolismo'],
                'grasso_viscerale': form.cleaned_data['grasso_viscerale'],
                'collocm': form.cleaned_data['collocm'],
                'toracecm': form.cleaned_data['toracecm'],
                'cosciadxcm': form.cleaned_data['cosciadxcm'],
                'cosciasxcm': form.cleaned_data['cosciasxcm'],
                'fianchicm': form.cleaned_data['fianchicm'],
                'addomecm': form.cleaned_data['addomecm'],
                'ginocchiodxcm': form.cleaned_data['ginocchiodxcm'],
                'ginocchiosxcm': form.cleaned_data['ginocchiosxcm'],
            }
            # aggioramenti dei dati del cliente
            dati_cliente = request.session['ultimo_utente']
            informazioni_cliente = {}
            if dati_cliente['altezza'] != form.cleaned_data['altezza']:
                informazioni_cliente['altezza'] = form.cleaned_data['altezza']

            if dati_cliente['cellulare'] != form.cleaned_data['cellulare']:
                informazioni_cliente['cellulare'] = form.cleaned_data['cellulare']

            if dati_cliente['email'] != form.cleaned_data['email']:
                informazioni_cliente['email'] = form.cleaned_data['email']

            if len(informazioni_cliente) != 0:

                url_backend = settings.BASE_URL + \
                    'cliente/clienti/'+str(dati_cliente['id'])+'/'
                headers = {
                    "Authorization": f"Token {request.session['auth_token']}"
                }
                response = requests.patch(
                    url_backend, data=informazioni_cliente, headers=headers)

                if response.status_code == 200:
                    request.session['ultimo_utente'] = response.json()
                elif response.status_code >= 400:
                    return redirect('erroreserver', status_code=response.status_code, text=response.text)
            # inserimento misura
            url_backend = settings.BASE_URL + 'cliente/clientimisure/'
            headers = {
                "Authorization": f"Token {request.session['auth_token']}"
            }
            response = requests.post(
                url_backend, data=misure, headers=headers)
            if response.status_code == 200 or response.status_code == 201:
                return redirect('clienti:misure_riepilogo_clienti', id=dati_cliente['id'])
            elif response.status_code >= 400:
                return redirect('erroreserver', status_code=response.status_code, text=response.text)
        else:

            return render(request, 'clienti/nuovamisura.html', {'form': form})
    else:

        if dati_cliente['altezza']:
            altezza = dati_cliente['altezza']
        else:
            altezza = 0

        formato = "%Y-%m-%d"
        data_di_nascita = datetime.strptime(
            dati_cliente['data_nascita'], formato)
        data_corrente = datetime.now()
        eta = data_corrente.year - data_di_nascita.year - \
            ((data_corrente.month, data_corrente.day) <
             (data_di_nascita.month, data_di_nascita.day))

        initial_data = {
            'cellulare': dati_cliente['cellulare'],
            'email': dati_cliente['email'],
            'altezza': altezza,
            'sesso': dati_cliente['sesso'],
            'eta': eta

        }
        form = FormMisure(initial=initial_data)

    return render(request, 'clienti/nuovamisura.html', {'form': form})


def riepilogo_misura(request, id):

    # richiamare cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # variabile per il campo peso desiderato
    if cliente['peso_desiderato']:
        peso_desiderato = cliente['peso_desiderato']
    else:
        peso_desiderato = 0

    if request.method == 'POST':
        form = FormMisureRiassunto(request.POST)
        pesoform = request.POST.get("peso_desiderato")

        if pesoform != peso_desiderato:

            misure = {
                'peso_desiderato': pesoform,
                'compilazione_pcu': True
            }
        else:

            misure = {
                'compilazione_pcu': True
            }
        # Effettua la richiesta Put all'API per aggiornare
        url_backend = settings.BASE_URL + \
            'cliente/clienti/'+str(id)+'/'
        headers = {
            "Authorization": f"Token {request.session['auth_token']}"}
        response = requests.patch(
            url_backend, data=misure, headers=headers)

        if response.status_code == 200:

            # Redirect alla lista dei clienti
            return redirect('clienti:inviopcu', id=id)
        elif response.status_code >= 400:
            return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # richiamare misure
    url_backend = settings.BASE_URL + 'cliente/misure/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        misure = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # richiamare nome misure
    url_backend = settings.BASE_URL + 'cliente/api/campi_misure/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        apimisure = response.json()

    # misure app
    misureapp = dati_cliente_misure(
        request, cliente['cellulare'], cliente['id'], cliente['id_utente_app'], cliente['lingua_utente'])

    if misureapp != False:
        misurepergrafico = misureapp
    else:
        misurepergrafico = []
    lista_opzioni = apimisure

    misuracopia = copy.deepcopy(misure)

    # aggiungo alle misure dell'app le misure che ho presenti nel sistema
    for misurainserita in misuracopia:

        data_input = misurainserita['data']

        data_datetime = datetime.strptime(
            data_input[0:19], '%Y-%m-%dT%H:%M:%S')

        del misurainserita['id']
        del misurainserita['data']
        del misurainserita['peso_ottimale']
        del misurainserita['cliente']

        for chiave, valore in misurainserita.items():

            for nomemisura in apimisure:

                if chiave in nomemisura:
                    nome = nomemisura[1]
                    break
                else:
                    nome = chiave

            nuovoelemento = {'data': data_datetime,
                             'valore': str(valore),
                             'misura': str(nome),
                             'app': False}

            misurepergrafico.append(nuovoelemento)

    # le ordino per data
    misure_ordinate = sorted(misurepergrafico, key=lambda x: x['data'])

    # preparo il json

    def custom_json_converter(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%d-%m-%Y')
        raise TypeError("Oggetto non serializzabile")
    lista_misure = json.dumps(misure_ordinate, default=custom_json_converter)

    # richiamare bmi
    bmi_ultima_misura = misure[-1]['bmi']
    url_backend = settings.BASE_URL + 'utils/statobmi/' + \
        str(id) + '/' + str(bmi_ultima_misura)

    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        stato_peso = response.json()

    form = FormMisureRiassunto(
        initial={'peso_ottimale': misure[-1]['peso_ottimale'], 'peso_desiderato': peso_desiderato}, lista_opzioni=lista_opzioni)

    return render(request, 'clienti/riassuntopc.html', {'form': form, 'misure_da_inserire': lista_misure, 'cliente': cliente, 'stato': stato_peso})


def inviopcu(request, id):

    risposta = False

    if request.method == 'POST':
        azione = request.POST.get('azione')
        chiave = get_random_string(length=10, allowed_chars='0123456789')
        if azione == 'sms':
            risposta = inviosms(request, chiave, id)
            request.session['firma_moduli_pcu'] = chiave
            # Esegui l'invio SMS
        elif azione == 'email':
            # idemail invio riassunto pcu 12
            idemail = 12
            risposta = inviomailchiave(request, chiave, id, idemail)
            request.session['firma_moduli_pcu'] = chiave
            print(chiave)
            # Esegui l'invio Email
        elif azione == 'chiave':
            chiave_inserita = request.POST.get('chiave')
            chiave = request.session['firma_moduli_pcu']
            if chiave == chiave_inserita:
                idemail = 13
                percorso = ModuloPersonal(request, id)
                risposta = inviomailallegato(request, percorso, id, idemail)
                # vedo se è un nuovocliente
                url_backend = settings.BASE_URL + \
                    'cliente/nuovocliente/'+str(id)+'/'
                headers = {
                    "Authorization": f"Token {request.session['auth_token']}"}
                response = requests.get(url_backend, headers=headers)
                if response.status_code == 200:
                    nuovocliente = response.json()
                elif response.status_code >= 400:
                    return redirect('erroreserver', status_code=response.status_code, text=response.text)

                if nuovocliente['misure']:

                    return render(request, 'ordini/email_successo.html', {'id': id})

                else:
                    return render(request, 'amministrazione/invioconsuccesso.html')

    form = FormChiave()
    context = {'id': id, 'inserimento': risposta, 'form': form}
    return render(request, 'clienti/invio.html', context)


def riepilogo_misura_elenco(request, id):

    # richiama cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # variabile per il campo peso desiderato
    if cliente['peso_desiderato']:
        peso_desiderato = cliente['peso_desiderato']
    else:
        peso_desiderato = 0

    if request.method == 'POST':
        form = FormMisureRiassunto(request.POST)
        pesoform = request.POST.get("peso_desiderato")

        if pesoform != peso_desiderato:

            misure = {
                'peso_desiderato': pesoform
            }
            # Effettua la richiesta Put all'API per aggiornare
            url_backend = settings.BASE_URL + \
                'cliente/clienti/'+str(id)+'/'
            headers = {
                "Authorization": f"Token {request.session['auth_token']}"}
            response = requests.patch(
                url_backend, data=misure, headers=headers)

            if response.status_code == 200:

                # Redirect alla lista dei clienti
                return redirect('clienti:inviopcu', id=id)
            elif response.status_code >= 400:
                return redirect('erroreserver', status_code=response.status_code, text=response.text)
        else:
            request.session['ultimo_utente'] = cliente
            return redirect('clienti:nuovamisura')

    # richiamare misure
    url_backend = settings.BASE_URL + 'cliente/misure/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        misure = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # richiamare cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # richiamare nome misure
    url_backend = settings.BASE_URL + 'cliente/api/campi_misure/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        apimisure = response.json()

    # misure app
    misureapp = dati_cliente_misure(
        request, cliente['cellulare'], cliente['id'], cliente['id_utente_app'], cliente['lingua_utente'])

    if misureapp != False:
        misurepergrafico = misureapp
    else:
        misurepergrafico = []
    lista_opzioni = apimisure

    misuracopia = copy.deepcopy(misure)

    # aggiungo alle misure dell'app le misure che ho presenti nel sistema
    for misurainserita in misuracopia:

        data_input = misurainserita['data']

        data_datetime = datetime.strptime(
            data_input[0:19], '%Y-%m-%dT%H:%M:%S')

        del misurainserita['id']
        del misurainserita['data']
        del misurainserita['peso_ottimale']
        del misurainserita['cliente']

        for chiave, valore in misurainserita.items():

            for nomemisura in apimisure:

                if chiave in nomemisura:
                    nome = nomemisura[1]
                    break
                else:
                    nome = chiave

            nuovoelemento = {'data': data_datetime,
                             'valore': str(valore),
                             'misura': str(nome),
                             'app': False}

            misurepergrafico.append(nuovoelemento)

    # le ordino per data
    misure_ordinate = sorted(misurepergrafico, key=lambda x: x['data'])

    # preparo il json

    def custom_json_converter(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%d-%m-%Y')
        raise TypeError("Oggetto non serializzabile")
    lista_misure = json.dumps(misure_ordinate, default=custom_json_converter)

    # richiamare bmi
    bmi_ultima_misura = misure[-1]['bmi']
    url_backend = settings.BASE_URL + 'utils/statobmi/' + \
        str(id) + '/' + str(bmi_ultima_misura)

    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        stato_peso = response.json()

    form = FormMisureRiassunto(
        initial={'peso_ottimale': misure[-1]['peso_ottimale'], 'peso_desiderato': peso_desiderato}, lista_opzioni=lista_opzioni)

    return render(request, 'clienti/riassuntopc.html', {'form': form, 'misure_da_inserire': lista_misure, 'cliente': cliente, 'stato': stato_peso})
