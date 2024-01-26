from distutils.command import clean
from multiprocessing import context
from turtle import pd
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator

from datetime import datetime

import requests
import re
import pdb

from Myw8ForAesthetics.decorators import handle_exceptions, handle_error_response
from amministrazione.views import inviomailchiave, inviosms, inviomailallegato, inviomailchiaveallegato
from .form import FormRateale
from clienti.form import FormChiave, ModuloInformazioniForm, AlimentiForm
from amministrazione.creapdfordini import moduloOrdine, moduloOrdineFirmato
from amministrazione.creapdfmoduli import moduloDati, moduloAlimenti, moduloDatiFirmato, moduloAlimentiFirmato
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

    # richiesta cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    # richiesta patologie nel sistema
    url_backend = settings.BASE_URL + 'cliente/listapatologie/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        patologie = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # suddivido patologie per sesso
    patologie_da_mostrare = []

    for patologia in patologie:
        if patologia['patologia_sesso'] == 'T':
            patologie_da_mostrare.append(patologia)
        else:
            if patologia['patologia_sesso'] == cliente['sesso']:
                patologie_da_mostrare.append(patologia)

    choices_patologie = [(patologia['id'], patologia['nome'])
                         for patologia in patologie_da_mostrare]

    if request.method == 'POST':
        form = ModuloInformazioniForm(request.POST)

        if form.is_valid():

            id_numerici_patologie = [
                int(patologia.split('_')[-1]) for patologia in form.cleaned_data['patologie']]

            dati = {
                'cliente': cliente['id'],
                'professione': form.cleaned_data['professione'],
                'stato_civile': form.cleaned_data['stato_civile'],
                'maggiorenne': form.cleaned_data['maggiorenne'],
                'peso_attuale': form.cleaned_data['peso_attuale'],
                'altezza': form.cleaned_data['altezza'],
                'bmi': form.cleaned_data['bmi'],
                'stato_attuale': form.cleaned_data['stato_attuale'],
                'peso_ottimale': form.cleaned_data['peso_ottimale'],
                'scostamento_peso': form.cleaned_data['scostamento_peso'],
                'peso_desiderato': form.cleaned_data['peso_desiderato'],
                'struttura_fisica': form.cleaned_data['struttura_fisica'],
                'struttura_desiderata': form.cleaned_data['struttura_desiderata'],
                'pressione_arteriosa': form.cleaned_data['pressione_arteriosa'],
                'diabete': form.cleaned_data['diabete'],
                'tipo_diabete': form.cleaned_data['tipo_diabete'],
                'menopausa': form.cleaned_data['menopausa'],
                'gravidanza': form.cleaned_data['gravidanza'],
                'mesi_gravidanza': form.cleaned_data['mesi_gravidanza'],
                'rapporto_corpo': form.cleaned_data['rapporto_corpo'],
                'droghe': form.cleaned_data['droghe'],
                'allergie': form.cleaned_data['allergie'],
                'allergie_elenco': form.cleaned_data['allergie_elenco'],
                'farmaci': form.cleaned_data['farmaci'],
                'farmaci_elenco': form.cleaned_data['farmaci_elenco'],
                'sport': form.cleaned_data['sport'],
                'sport_praticato': form.cleaned_data['sport_praticato'],
                'sport_praticato_giorni': form.cleaned_data['sport_praticato_giorni'],
                'gruppo_sanguigno': form.cleaned_data['gruppo_sanguigno'],
                'insonnia': form.cleaned_data['insonnia'],
                'stitichezza': form.cleaned_data['stitichezza'],
                'fame_nervosa': form.cleaned_data['fame_nervosa'],
                'fumo': form.cleaned_data['fumo'],
                'numero_sigarette': form.cleaned_data['numero_sigarette'],
                'delta_numero_sigarette': form.cleaned_data['delta_numero_sigarette'],
                'gengive': form.cleaned_data['gengive'],
                'tatuaggi': form.cleaned_data['tatuaggi'],
                'bevi_acqua': form.cleaned_data['bevi_acqua'],
                'litri_acqua': form.cleaned_data['litri_acqua'],
                'filosofia_alimentare': form.cleaned_data['filosofia_alimentare'],
                'maiale': form.cleaned_data['maiale'],
                'figli': form.cleaned_data['figli'],
                'numero_figli': form.cleaned_data['numero_figli'],
                'pasto_condiviso': form.cleaned_data['pasto_condiviso'],
                'alimenti_preferiti': ', '.join(form.cleaned_data['alimenti_preferiti']),
                'gusti_preferiti': ', '.join(form.cleaned_data['gusti_preferiti']),
                'patologie': id_numerici_patologie,
                'problemi_cardiaci': form.cleaned_data['problemi_cardiaci'],
                'problem_cardiaci_tipo': form.cleaned_data['problem_cardiaci_tipo'],
                'sicura': form.cleaned_data['sicura'],
                'felice': form.cleaned_data['felice'],
                'stress': form.cleaned_data['stress'],
                'paure': form.cleaned_data['paure'],
                'lutti': form.cleaned_data['lutti'],
                'incubi': form.cleaned_data['incubi'],
                'stanco': form.cleaned_data['stanco'],
                'rabbia': form.cleaned_data['rabbia'],
                'sfogo': form.cleaned_data['sfogo'],
                'colpa': form.cleaned_data['colpa'],
                'piangi': form.cleaned_data['piangi'],
                'carattere1': form.cleaned_data['carattere1'],
                'carattere2': form.cleaned_data['carattere2'],
                'carattere3': form.cleaned_data['carattere3'],
                'determinato': form.cleaned_data['determinato'],
                'amici_dieta': form.cleaned_data['amici_dieta'],
                'note': form.cleaned_data['note'],
            }

            # Effettua la richiesta POST all'API
            url_backend = settings.BASE_URL + 'cliente/inserisciinfo/'
            headers = {
                "Authorization": f"Token {request.session['auth_token']}"
            }
            response = requests.post(
                url_backend, json=dati, headers=headers)

            if response.status_code == 201:  # Status code per "Created"

                return redirect('ordini:moduloalimenti_mancante', id=id)
            elif response.status_code >= 400:
                return redirect('erroreserver', status_code=response.status_code, text=response.text)

        else:
            form.fields['patologie'].choices = choices_patologie
            context = {
                'form': form,
                'cliente': cliente,
            }
            print(form.errors)
            return render(request, 'ordini/moduloinfo.html', context)

    form = ModuloInformazioniForm(initial={
                                  'altezza': cliente['altezza'], 'peso_desiderato': cliente['peso_desiderato']})
    form.fields['patologie'].choices = choices_patologie
    context = {
        'form': form,
        'cliente': cliente,

    }

    return render(request, 'ordini/moduloinfo.html', context)


def moduloalimenti_mancante(request, id):

    url_backend = settings.BASE_URL + 'cliente/gusti/'+str(id)+'/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        gusti = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    url_backend = settings.BASE_URL + 'cliente/listaalimenti/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        alimenti = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    lista_di_alimenti = alimenti

    # if gusti['filosofia_alimentare'] == 'Vegetariano':

    #     elementi_da_rimuovere = ['Agnello', 'Coniglio', 'Crostacei', 'Maiale',
    #                              'Manzo', 'Molluschi', 'Pesce', 'Pollo', 'Tacchino', 'Vitello']

    # # Filtra gli elementi rimuovendo quelli con 'nome' o 'classe_alimenti' nei valori da rimuovere
    #     lista_di_alimenti_filtrata = [
    #         alimento for alimento in lista_di_alimenti if alimento['classe_alimenti'] not in elementi_da_rimuovere]
    # else:
    #     if gusti['maile'] == 'No':

    #         lista_di_alimenti_filtrata = [
    #             alimento for alimento in lista_di_alimenti if alimento['classe_alimenti'] != 'Maiale']
    #     else:

    lista_di_alimenti_filtrata = lista_di_alimenti

    if request.method == 'POST':

        # se non ci sono elementi selezionati deve passare alla prossima pagina
        alimenti_selezionati = request.POST.getlist('alimenti_selezionati')
        if not alimenti_selezionati:
            return redirect('ordini:invio_moduli_mail', id=id)
        else:
            allergia = request.POST.getlist('allergia')

            for alimento in alimenti_selezionati:
                if alimento in allergia:
                    pericolo = True
                else:
                    pericolo = False

                dati = {
                    'cliente': id,
                    'alimento': alimento,
                    'allergia': pericolo
                }

                url_backend = settings.BASE_URL + 'cliente/inserimentogusti/'
                headers = {
                    "Authorization": f"Token {request.session['auth_token']}"
                }
                response = requests.post(
                    url_backend, json=dati, headers=headers)
                # puo dare errore per ogni inserimento
                if response.status_code >= 400:
                    return redirect('erroreserver', status_code=response.status_code, text=response.text)

            # se è vegetariano inserisco in automatico gli elementi non graditi
            if gusti['filosofia_alimentare'] == 'Vegetariano':

                lista_di_alimenti_da_eliminare = [
                    alimento for alimento in lista_di_alimenti if alimento['classe_alimenti'] in elementi_da_rimuovere]
            # elimino il maiale
            elif gusti['maile'] == 'No':

                lista_di_alimenti_da_eliminare = [
                    alimento for alimento in lista_di_alimenti if alimento['classe_alimenti'] == 'Maiale']

            else:
                lista_di_alimenti_da_eliminare = []

            if lista_di_alimenti_da_eliminare:
                for alimento in lista_di_alimenti_da_eliminare:

                    dati = {
                        'cliente': id,
                        'alimento': alimento['id'],
                        'allergia': False
                    }

                    url_backend = settings.BASE_URL + 'cliente/inserimentogusti/'
                    headers = {
                        "Authorization": f"Token {request.session['auth_token']}"
                    }
                    response = requests.post(
                        url_backend, json=dati, headers=headers)
                    # puo dare errore per ogni inserimento
                    if response.status_code >= 400:
                        return redirect('erroreserver', status_code=response.status_code, text=response.text)

            return redirect('ordini:invio_moduli_mail', id=id)

    context = {

        'alimenti': lista_di_alimenti_filtrata

    }

    return render(request, 'ordini/moduloalimenti.html', context)


def invio_moduli(request, id):

    risposta = False
    if request.method == 'POST':

        azione = request.POST.get('azione')
        chiave = get_random_string(length=10, allowed_chars='0123456789')
        if azione == 'sms':
            risposta = inviosms(request, chiave, id)
            request.session['firma_moduli_dati'] = chiave
            # Esegui l'invio SMS
        elif azione == 'email':
            # idemail invio moduli info
            idemail = 10
            percorso1 = moduloDati(request, id)
            percorso2 = moduloAlimenti(request, id)
            percorso = dict(percorso1, **percorso2)

            risposta = inviomailchiaveallegato(
                request, chiave, percorso, id, idemail)
            request.session['firma_moduli_dati'] = chiave
            print(chiave)
            # Esegui l'invio Email
        elif azione == 'chiave':
            chiave_inserita = request.POST.get('chiave')
            chiave = request.session['firma_moduli_dati']
            if chiave == chiave_inserita:
                # idemail invio moduli info firmato
                idemail = 9
                percorso1 = moduloDatiFirmato(request, id)
                percorso2 = moduloAlimentiFirmato(request, id)
                percorso = dict(percorso1, **percorso2)
                print(percorso)
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
                    return render(request, 'ordini/email_successo_moduli.html')
                else:
                    return redirect('ordini:modulodati_mancante', id=id)

    form = FormChiave()
    context = {'id': id, 'inserimento': risposta, 'form': form}
    return render(request, 'ordini/invio_moduli.html', context)


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

    url_backend = settings.BASE_URL + 'ordini/dettagli/' + str(id)
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        ordini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    context = {'programma': ordini}
    print(ordini)
    return render(request, 'ordini/informazione_ordine.html', context)
