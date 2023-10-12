from django.shortcuts import render, redirect
from django.conf import settings

from datetime import datetime

import requests

from Myw8ForAesthetics.decorators import handle_exceptions, handle_error_response
# Create your views here.


@handle_exceptions
def sceltaprogramma(request, id):

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
    
    #se il cliente non a il modulo lo deve compilare
    if  cliente['compilazione_pcu'] == False:
        
        request.session['ultimo_utente'] = cliente
        return redirect('ordini:misura_mancante')
    else:
        request.session['cliente_ordine'] = cliente
        #richiamo il numero e il tipo di ordini effettuati
        url_backend = settings.BASE_URL + 'ordini/tipo_ordini/'+str(id)

        headers = {
            "Authorization": f"Token {request.session['auth_token']}"
        }
        response = requests.get(url_backend, headers=headers)
        
        if response.status_code == 200:
            tipo_ordine = response.json()
        elif response.status_code >= 400:
            return redirect('erroreserver', status_code=response.status_code, text=response.text)
        import pdb;
        pdb.set_trace()
        #caso nessun ordine inserito nel sistema per il cliente
        if tipo_ordine['ordini'] == 'nessuno':
            a =0
        #caso un ordine small inserito nel sistema per il cliente
        elif tipo_ordine['ordini'] == 'solo_test':
            a =0 
        #caso un ordine non smal inserito nel sistema per il cliente
        elif tipo_ordine['ordini'] == 'completo':    
            a=0
        #caso piu ordini inseriti nel sistema per il cliente
        else:
            a=0
            
            
        #se ha un beneficiario vado sui programmi kids
       
        
        
        
       
      

        
        request.session['cliente_ordine_eta'] = minorenne

        url_backend = settings.BASE_URL + 'listini/lista/' + str(minorenne)
        headers = {"Authorization": f"Token {request.session['auth_token']}"}
        response = requests.get(url_backend, headers=headers)
        if response.status_code == 200:
            listini = response.json()
        elif response.status_code >= 400:
            return redirect('erroreserver', status_code=response.status_code, text=response.text)

        context = {'dati': listini, 'minore': minorenne}

        return render(request, 'ordini/scelta_gruppo.html', context)


    
        

@handle_exceptions
def sceltalistino(request, id):

    url_backend = settings.BASE_URL + 'listini/sceltaprogrammi/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    minore = request.session['cliente_ordine_eta']
    params = {'minore': minore, 'id': id}

    
    
    response = requests.get(url_backend, headers=headers, params=params)
    if response.status_code == 200:
        listini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    
    context = {'dati': listini, 'minore': minore}

    return render(request, 'ordini/scelta_programma.html', context)



def misure_mancanti(request):
    
     return render(request, 'ordini/misura_mancante.html')
