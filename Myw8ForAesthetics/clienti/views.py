import string
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, View
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from codicefiscale import codicefiscale

import requests

from Myw8ForAesthetics.decorators import handle_exceptions, handle_error_response
from .models import Cliente
from .form import FormCliente, FormClientePiva, FormClienteMinore
from .form import ClientiSearchForm


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
            payload = {
                'nome': form.cleaned_data['nome'],
                'cognome': form.cleaned_data['cognome'],
                'citta_nascita': form.cleaned_data['citta_nascita'],
                'data_nascita': form.cleaned_data['data_nascita'],
                'indirizzo': form.cleaned_data['indirizzo'],
                'cap': form.cleaned_data['cap'],
                'citta': form.cleaned_data['citta'],
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
                url_backend, data=payload, headers=headers)
            print(response.status_code)
            if response.status_code == 201:  # Status code per "Created"
                # Redirect alla lista dei clienti o dove preferisci
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
            payload = {
                'nome': form.cleaned_data['nome'],
                'cognome': form.cleaned_data['cognome'],
                'citta_nascita': form.cleaned_data['citta_nascita'],
                'data_nascita': form.cleaned_data['data_nascita'],
                'indirizzo': form.cleaned_data['indirizzo'],
                'cap': form.cleaned_data['cap'],
                'citta': form.cleaned_data['citta'],
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
                url_backend, data=payload, headers=headers)

            if response.status_code == 201:  # Status code per "Created"
                # Redirect alla lista dei clienti o dove preferisci
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
            payload = {
                'nome': form.cleaned_data['nome'],
                'cognome': form.cleaned_data['cognome'],
                'citta_nascita': form.cleaned_data['citta_nascita'],
                'data_nascita': form.cleaned_data['data_nascita'],
                'indirizzo': form.cleaned_data['indirizzo'],
                'cap': form.cleaned_data['cap'],
                'citta': form.cleaned_data['citta'],
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
                url_backend, data=payload, headers=headers)

            if response.status_code == 201:  # Status code per "Created"
                # Redirect alla lista dei clienti o dove preferisci
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


@handle_exceptions
def info_cliente(request, id):
    print('pene')
    # prendo l'url il token echiamp il server per il cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'

    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    print('prova')
    print(request.session['user_id'])
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
                    'data_nascita': form.cleaned_data['data_nascita'],
                    'indirizzo': form.cleaned_data['indirizzo'],
                    'cap': form.cleaned_data['cap'],
                    'citta': form.cleaned_data['citta'],
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
                    'data_nascita': form.cleaned_data['data_nascita'],
                    'indirizzo': form.cleaned_data['indirizzo'],
                    'cap': form.cleaned_data['cap'],
                    'citta': form.cleaned_data['citta'],
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
                    print('ciao')
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
                payload = {
                    'nome': form.cleaned_data['nome'],
                    'cognome': form.cleaned_data['cognome'],
                    'citta_nascita': form.cleaned_data['citta_nascita'],
                    'data_nascita': form.cleaned_data['data_nascita'],
                    'indirizzo': form.cleaned_data['indirizzo'],
                    'cap': form.cleaned_data['cap'],
                    'citta': form.cleaned_data['citta'],
                    'codice_fiscale': form.cleaned_data['codice_fiscale'],
                    'telefono': form.cleaned_data['telefono'],
                    'cellulare': form.cleaned_data['cellulare'],
                    'email': form.cleaned_data['email'],
                    'sesso': form.cleaned_data['sesso'],
                    'note': form.cleaned_data['note'],
                }

                # Effettua la richiesta Put all'API per aggiornare

                response = requests.put(
                    url_backend, data=payload, headers=headers)
                print('ciao')

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
