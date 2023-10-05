from django.shortcuts import render, redirect
from django.conf import settings

import requests

from Myw8ForAesthetics.decorators import handle_exceptions, handle_error_response
# Create your views here.


@handle_exceptions
def sceltaprogramma(request):

    url_backend = settings.BASE_URL + 'listini/lista/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        listini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    print(listini)
    context = {'dati': listini}

    return render(request, 'ordini/scelta_programma.html', context)
