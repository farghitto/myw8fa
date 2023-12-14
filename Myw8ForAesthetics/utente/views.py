import pdb
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
import requests

from Myw8ForAesthetics.decorators import handle_exceptions, verifica_connessione


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
            request.session['username'] = username
            request.session['password'] = password
            
            

            return redirect('utente:homec')

        else:

            form_errors['Username'] = 'Credenziali non valide. Riprova'
            form_errors['Password'] = 'Credenziali non valide. Riprova'
            return render(request, 'utente/login.html', {'error': 'si', 'form_errors': form_errors})

    else:
        return render(request, 'utente/login.html')


@verifica_connessione
def homepagecentro(request):

    return render(request, 'utente/homepagecentro.html')


@handle_exceptions
def erroreserver(request, status_code, text):

    context = {'codice_di_errore': status_code,
               'dettaglio': text
               }

    return render(request, 'utente/erroreserver.html', context)


@handle_exceptions
def logout_view(request):

    url_backend = settings.BASE_URL + 'logout'
    token = request.session['auth_token']
    headers = {
        "Authorization": f"Token {token}"
    }
    if 'auth_token' in request.session:
        del request.session['auth_token']
    response = requests.post(
        url_backend, headers=headers)

    if response.status_code == 200:

        return redirect('utente:login')
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)


def logout_auto_view(request):

    url_backend = settings.BASE_URL + 'logout'
    token = request.session['auth_token']
    request.session.flush()
    risposta = delete_cookie_view(request)
    headers = {
        "Authorization": f"Token {token}"
    }

    response = requests.post(
        url_backend, headers=headers)

    print('ok')


def delete_cookie_view(request):
    # Crea una risposta vuota
    response = HttpResponse()
    cookie_name = request.session.get_cookie_name('auth_token')
    # Cancella un cookie specifico impostando la data di scadenza nel passato
    response.delete_cookie('cookie_name')

    # Restituisci la risposta con il cookie eliminato
    return response
