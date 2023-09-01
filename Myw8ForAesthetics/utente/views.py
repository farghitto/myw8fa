from django.shortcuts import render, redirect
from django.conf import settings

import requests

from Myw8ForAesthetics.decorators import handle_exceptions


def login_view(request):
    if request.method == 'POST':

        # import pdb; pdb.set_trace()

        username = request.POST['Username']
        password = request.POST['Password']
        form_errors = {}

        # controllo se username e password sono inseriti
        if not username:
            form_errors['Username'] = 'Campo Username obbligatorio'
            return render(request, 'utente/login.html', {'error': 'si', 'form_errors': form_errors})

        if not password:
            form_errors['Password'] = 'Campo Password obbligatorio'
            return render(request, 'utente/login.html', {'error': 'si', 'form_errors': form_errors})

        # L'URL dell'endpoint di autenticazione
        url = settings.BASE_URL + 'autenticazione'
        data = {
            "username": username,
            "password": password
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:

            token = response.json()["token"]
            user_id = response.json()["user_id"]

            request.session['auth_token'] = token
            request.session['user_id'] = user_id

            return redirect('utente:homec')

        else:

            form_errors['Username'] = 'Credenziali non valide. Riprova'
            form_errors['Password'] = 'Credenziali non valide. Riprova'
            return render(request, 'utente/login.html', {'error': 'si', 'form_errors': form_errors})

    else:
        return render(request, 'utente/login.html')


def homepagecentro(request):

    return render(request, 'utente/homepagecentro.html')


@handle_exceptions
def erroreserver(request, status_code, text):

    context = {'codice_di_errore': status_code,
               'dettaglio': text
               }

    return render(request, 'utente/erroreserver.html', context)
