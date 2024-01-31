import imp
import pdb
import re
import requests

from django.shortcuts import render, redirect, get_object_or_404

from django.conf import settings

from clienti.models import AnagraficaCliente, PersonalCheckUpCliente


def estrai_numero(input_string):
    # Utilizza un'espressione regolare per trovare il primo numero nella stringa
    match = re.search(r'\d+', input_string)

    # Se un numero è stato trovato, restituiscilo come intero, altrimenti restituisci None
    if match:
        numero = int(match.group())
        return numero
    else:
        return ' '


def elimina_numero(input_string):
    # Utilizza un'espressione regolare per sostituire il numero con una stringa vuota
    nuova_stringa = re.sub(r'\d+', '', input_string)
    return nuova_stringa


def crea_cliente_myoffice(request, dati):

    indirizzo = dati['indirizzo']
    numero_civico = estrai_numero(indirizzo)
    indirizzo_senza_civico = elimina_numero(indirizzo)

    dati_da_inviare = {

        'nome': dati['nome'],
        'cognome': dati['cognome'],
        'citta_nascita': dati['citta_nascita'],
        'data_nascita': dati['data_nascita'],
        'indirizzo': indirizzo_senza_civico,
        'numero_civico': numero_civico,
        'cap': dati['cap'],
        'citta': dati['citta'],
        'codice_fiscale': dati['codice_fiscale'],
        'telefono': dati['telefono'],
        'cellulare': dati['cellulare'],
        'email': dati['email'],
        'sesso': dati['sesso'],
        'note': dati['note'],
        'consulente_id': request.session['user_id']

    }

    if 'ragione_sociale' in dati:

        nuovi_dati = {
            'ragione_sociale': dati['ragione_sociale'],
            'sede': dati['sede'],
            'indirizzo_sede': dati['indirizzo_sede'],
            'cap_sede': dati['cap_sede'],
            'telefono_sede': dati['telefono_sede'],
            'email_sede': dati['email_sede'],
            'partita_iva': dati['partita_iva'],
            'codice_univoco': dati['codice_univoco'],
        }

        dati_da_inviare.update(nuovi_dati)

    if 'beneficiario_nome' in dati:

        nuovi_dati = {
            'beneficiario_nome': dati['beneficiario_nome'],
            'beneficiario_cognome': dati['beneficiario_cognome'],
            'beneficiario_codice_fiscale': dati['beneficiario_codice_fiscale'],
            'beneficiario_cellulare': dati['beneficiario_cellulare'],
        }

        dati_da_inviare.update(nuovi_dati)

    nuovo_cliente = AnagraficaCliente.objects.create(**dati_da_inviare)
    nuovo_cliente.save()
    
    id = nuovo_cliente.id
    
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'

    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    
    dati = {       
        'id_utente_myoffice' : id      
    }
       
    response = requests.put(
                    url_backend, data=dati, headers=headers)
    

    return True


def modifica_cliente_myoffice(request, dati, id):

    indirizzo = dati['indirizzo']
    numero_civico = estrai_numero(indirizzo)
    indirizzo_senza_civico = elimina_numero(indirizzo)

    cliente = get_object_or_404(AnagraficaCliente, id=id)

    cliente.nome = dati['nome']
    cliente.cognome = dati['cognome']
    cliente.citta_nascita = dati['citta_nascita']
    cliente.data_nascita = dati['data_nascita']
    cliente.indirizzo = indirizzo_senza_civico
    cliente.numero_civico = numero_civico
    cliente.cap = dati['cap']
    cliente.citta = dati['citta']
    cliente.codice_fiscale = dati['codice_fiscale']
    cliente.telefono = dati['telefono']
    cliente.cellulare = dati['cellulare']
    cliente.email = dati['email']
    cliente.sesso = dati['sesso']
    cliente.note = dati['note']

    if 'ragione_sociale' in dati:

        cliente.ragione_sociale = dati['ragione_sociale']
        cliente.sede = dati['sede']
        cliente.indirizzo_sede = dati['indirizzo_sede']
        cliente.cap_sede = dati['cap_sede']
        cliente.telefono_sede = dati['telefono_sede']
        cliente.email_sede = dati['email_sede']
        cliente.partita_iva = dati['partita_iva']
        cliente.codice_univoco = dati['codice_univoco']

    if 'beneficiario_nome' in dati:

        cliente.beneficiario_nome = dati['beneficiario_nome']
        cliente.beneficiario_cognome = dati['beneficiario_cognome']
        cliente.beneficiario_codice_fiscale = dati['beneficiario_codice_fiscale']
        cliente.beneficiario_cellulare = dati['beneficiario_cellulare']

    cliente.save()

    return True


def aggiungi_modifica_myoffice(dati, id):

    cliente = get_object_or_404(AnagraficaCliente, id=id)

    if 'altezza' in dati:

        cliente.altezza = dati['altezza']

    if 'cellulare' in dati:

        cliente.cellulare = dati['cellulare']

    if 'email' in dati:

        cliente.email = dati['email']

    cliente.save()

    return True


def inserisci_misure_myoffice(dati, id):
    
    misure = {
                'cliente': id,
                'peso': dati['peso'],
                'altezza': dati['altezza'],
                'bmi': dati['bmi'],
                'grasso_corporeo': dati['grasso_corporeo'],
                'muscolatura': dati['muscolatura'],
                'metabolismo': dati['metabolismo'],
                'grasso_viscerale': dati['grasso_viscerale'],
                'collocm': dati['collocm'],
                'toracecm': dati['toracecm'],
                'cosciadxcm': dati['cosciadxcm'],
                'cosciasxcm': dati['cosciasxcm'],
                'fianchicm': dati['fianchicm'],
                'addomecm': dati['addomecm'],
                'ginocchiodxcm': dati['ginocchiodxcm'],
                'ginocchiosxcm': dati['ginocchiosxcm'],
            }
    
    nuova_misura = PersonalCheckUpCliente.objects.create(**misure)
    nuova_misura.save()
    
    return True