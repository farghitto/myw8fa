from django.shortcuts import render, redirect
from django.views.generic import CreateView

from django.http import JsonResponse
from django.urls import reverse_lazy

from codicefiscale import codicefiscale

from .models import Cliente
from .form import FormCliente, FormClientePiva, FormClienteMinore
from .form import ClientiSearchForm


def sceltacliente(request):

    return render(request, 'clienti/opzioniclienti.html')

def sceltamenu(request):

    return render(request, 'clienti/sceltaregistrazione.html')

def sceltapostcliente(request):

    return render(request, 'clienti/sceltadoporegistrazione.html')


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


def search_clienti(request):
    
    form = ClientiSearchForm(request.GET)
    risultato = []

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        risultato = Cliente.objects.filter(cognome__istartswith=search_query)
    else:    
        risultato = Cliente.objects.all()

    return render(request, 'clienti\elencoclienti.html', {'form': form, 'risultato': risultato})