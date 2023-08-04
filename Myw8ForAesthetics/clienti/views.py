from django.shortcuts import render, redirect


def sceltacliente(request):

    return render(request, 'clienti/opzioniclienti.html')


def sceltamenu(request):

    return render(request, 'clienti/sceltaregistrazione.html')


