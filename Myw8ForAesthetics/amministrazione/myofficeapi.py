import imp
import pdb
import re
import requests

from django.shortcuts import render, redirect

from django.conf import settings

from clienti.models import AnagraficaCliente


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






def crea_cliente_myoffice (request, dati):
    
    indirizzo = dati['indirizzo']
    numero_civico = estrai_numero(indirizzo)
    indirizzo_senza_civico = elimina_numero(indirizzo)
    
    dati_da_inviare = {
        
        'nome': dati['nome'],
        'cognome':dati['cognome'],
        'citta_nascita':dati['citta_nascita'], 
        'data_nascita':dati['data_nascita'],
        'indirizzo':indirizzo_senza_civico,
        'numero_civico': numero_civico,
        'cap':dati['cap'],
        'citta':dati['citta'],
        'codice_fiscale':dati['codice_fiscale'],
        'telefono':dati['telefono'],
        'cellulare':dati['cellulare'],
        'email':dati['email'],
        'sesso':dati['sesso'],
        'note':dati['note'],
        'consulente_id': request.session['user_id']
        
    }
    
    if 'ragione_sociale' in dati:
        
        nuovi_dati ={
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
        
        nuovi_dati ={
               'beneficiario_nome': dati['beneficiario_nome'],
                'beneficiario_cognome': dati['beneficiario_cognome'],
                'beneficiario_codice_fiscale': dati['beneficiario_codice_fiscale'],
                'beneficiario_cellulare': dati['beneficiario_cellulare'],
        }
        
        dati_da_inviare.update(nuovi_dati)
    
    nuovo_cliente = AnagraficaCliente.objects.create(**dati_da_inviare)
    nuovo_cliente.save()
    
    pdb.set_trace()
        
 

    
    return True





