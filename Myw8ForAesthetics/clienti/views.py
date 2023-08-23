from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from codicefiscale import codicefiscale

import requests

from .models import Cliente
from .form import FormCliente, FormClientePiva, FormClienteMinore
from .form import ClientiSearchForm


def sceltacliente(request):

    return render(request, 'clienti/opzioniclienti.html')

def sceltamenu(request):

    return render(request, 'clienti/sceltaregistrazione.html')

def sceltapostcliente(request):

    return render(request, 'clienti/sceltadoporegistrazione.html')


""" class CreaClienteView(View):
    
    template_name = 'clienti/nuovocliente.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        base_url = 'http://127.0.0.1:8000/'  # L'URL base del tuo server
        clienti_endpoint = 'clienti/lista'  # L'endpoint API per la creazione

        # Recupera i dati dal form
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        # Altri campi dati...

        # Crea il payload da inviare al server
        payload = {
            'nome': nome,
            'cognome': cognome,
            # Altri campi dati...
        }

        # Effettua la richiesta POST all'endpoint API
        response = requests.post(base_url + clienti_endpoint, data=payload)

        if response.status_code == 201:
            return redirect('clienti:postcliente')  # Redirect dopo la creazione
        else:
            error_message = "Errore nella creazione del cliente"
            return render(request, self.template_name, {'error_message': error_message}) """


class ClienteView(CreateView):  # classe per la creazione del cliente

    model = Cliente
    form_class = FormCliente
    template_name = 'clienti/nuovocliente.html'
    success_url = reverse_lazy ('clienti:postcliente')


class ClientePivaView(CreateView):  # classe per la creazione del cliente

    model = Cliente
    form_class = FormClientePiva
    template_name = 'clienti/nuovoclientepiva.html'
    success_url = reverse_lazy ('clienti:postcliente')

class ClienteMinoreView(CreateView):  # classe per la creazione del cliente

    model = Cliente
    form_class = FormClienteMinore
    template_name = 'clienti/nuovoclienteminore.html'
    success_url = reverse_lazy ('clienti:postcliente')



def get_codice_fiscale(request):
    
    cognome = request.GET.get('cognome')
    nome= request.GET.get('nome')
    sesso = request.GET.get('sesso')
    datanascita= request.GET.get('data')
    comune = request.GET.get('comune')
    
    try:
        cf =codicefiscale.encode    (
                                        lastname  =cognome,
                                        firstname = nome,
                                        gender = sesso,
                                        birthdate = datanascita,
                                        birthplace =comune,
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

def crea_cliente(request):
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
            response = requests.post(url_backend, data=payload)

            if response.status_code == 201:  # Status code per "Created"
                return redirect('clienti:postcliente')  # Redirect alla lista dei clienti o dove preferisci

    else:
        form = FormCliente()

    return render(request, 'clienti/nuovocliente.html', {'form': form})


def search_clienti(request):
    
    form = ClientiSearchForm(request.GET)
    
    url_backend = settings.BASE_URL + 'cliente/lista'

    response = requests.get(url_backend)
    if response.status_code == 200:
            clienti = response.json()
    
    """ return render(request, 'errore.html') """

    if form.is_valid():
        
        search_query = form.cleaned_data['search_query']
        elementi =  [cliente for cliente in clienti if cliente['cognome'].lower().startswith(search_query.lower())]
        
    else:   
         
        elementi = clienti
    
    
    # Imposta il numero di elementi da visualizzare per pagina
    paginator = Paginator(elementi, 8)  # Ad esempio, 10 elementi per pagina
    
    page_number = request.GET.get('page')  # Ottieni il numero di pagina dalla query string
    page_obj = paginator.get_page(page_number)
      
    context = {
        'page_obj': page_obj,
        'elementi': elementi,
        'form': form
        }

    return render(request, 'clienti\elencoclienti.html', context)