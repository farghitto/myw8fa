from django.shortcuts import render, redirect
from django.views.generic import CreateView

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
