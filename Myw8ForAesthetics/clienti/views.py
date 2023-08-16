from django.shortcuts import render, redirect
from django.views.generic import CreateView

from django.http import JsonResponse

from codicefiscale import codicefiscale

from .models import Cliente
from .form import FormCliente


def sceltacliente(request):

    return render(request, 'clienti/opzioniclienti.html')


def sceltamenu(request):

    return render(request, 'clienti/sceltaregistrazione.html')


class ClienteView(CreateView):  # classe per la creazione del cliente

    model = Cliente
    form_class = FormCliente
    template_name = 'clienti/nuovocliente.html'
    success_url = '/clienti/elencoclienti'



    def form_valid(self, form):

        dati = form.save(commit=False)
        dati.data_nascita = form.cleaned_data['data_di_nascita']
        dati.save()
        return super().form_valid(form)



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