from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings

import base64
import requests
import json

# Create your views here.


def inviomailchiave(request, chiave, id, idemail):

    # richiamo cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # richiamo email
    url_backend = settings.BASE_URL + 'utils/email/' + str(idemail)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        emailAzienda = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    subject = emailAzienda['testo_oggetto']
    from_email = emailAzienda['email']
    to = cliente['email']
    text_content = "Gentile " + cliente['cognome'] + " " + cliente['nome'] + \
        '\n' + emailAzienda['testo_mail'] + '\n' + chiave  # messaggio
        
        
    

    # caso email senza bcc
    if emailAzienda['bcc'] == None:
        email = EmailMessage(subject, text_content, from_email, [to])
    # caso email con bcc
    elif emailAzienda.bcc2 == None:
        bcc_addresses = [emailAzienda.bcc]
        email = EmailMessage(subject, text_content,
                             from_email, [to], bcc=bcc_addresses)
    # caso email con due bcc
    else:
        bcc_addresses = [emailAzienda.bcc, emailAzienda.bcc2]
        email = EmailMessage(subject, text_content,
                             from_email, [to], bcc=bcc_addresses)

    email.send()
    try:
        num_email_inviati = 2
        ritorno = True
    except:
        ritorno = False

    return ritorno


def inviosms(request, chiave, id):

    # richiamo cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    user = 'infomyw8'
    password = 'WRfv24#$'

    # concatena le credenziali con il carattere ':'
    credentials = f"{user}:{password}"

    # codifica le credenziali in base64
    encoded_credentials = base64.b64encode(
        credentials.encode('utf-8')).decode('utf-8')

    # crea l'header di autorizzazione con il valore base64
    authorization_header = f"Basic {encoded_credentials}"
    url = 'https://dashboard.wausms.com/Api/rest/message'

    # definisce gli header della richiesta
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': authorization_header
    }

    cellulare = cliente['cellulare']
    # definisce i dati da inviare come corpo della richiesta
    data = {
        'to': ['39'+str(cellulare)],
        'text': 'Grazie di averci accordado la tua fiducia, il codice da comunicare è :' + str(chiave),
        'from': 'W.T.A. MyW8'
    }

    # converte i dati in formato JSON
    json_data = json.dumps(data)

    # esegue la richiesta HTTP POST con gli header e i dati specificati
    response = requests.post(url, headers=headers, data=json_data)

    ritorno = False

    if response.status_code == 200:
        ritorno = True
    return ritorno


def inviomailallegato(request, percorso, id, idemail):

    # richiamo cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # richiamo email ()
    url_backend = settings.BASE_URL + 'utils/email/' + str(idemail)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        emailAzienda = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    subject = emailAzienda['testo_oggetto']
    from_email = emailAzienda['email']
    to = cliente['email']
    text_content = "Gentile " + cliente['cognome'] + " " + cliente['nome'] + \
        '\n' + emailAzienda['testo_mail'] + '\n'  # messaggio

    # caso email senza bcc
    if emailAzienda['bcc'] == None:
        email = EmailMessage(subject, text_content, from_email, [to])
    # caso email con bcc
    elif emailAzienda['bcc2'] == None:
        bcc_addresses = [emailAzienda['bcc']]
        email = EmailMessage(subject, text_content,
                             from_email, [to], bcc=bcc_addresses)
    # caso email con due bcc
    else:
        bcc_addresses = [emailAzienda['bcc'], emailAzienda['bcc2']]
        email = EmailMessage(subject, text_content,
                             from_email, [to], bcc=bcc_addresses)
    email.attach_file(percorso)
    email.send()
    try:
        num_email_inviati = 2
        ritorno = True
    except:
        ritorno = False

    return ritorno



def inviomailchiaveallegato(request, chiave, percorso, id, idemail):

    # richiamo cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # richiamo email
    url_backend = settings.BASE_URL + 'utils/email/' + str(idemail)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        emailAzienda = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    subject = emailAzienda['testo_oggetto']
    from_email = emailAzienda['email']
    to = cliente['email']
    text_content = "Gentile " + cliente['cognome'] + " " + cliente['nome'] + \
        '\n' + emailAzienda['testo_mail'] + '\n' + chiave  # messaggio
        
    
    # caso email senza bcc
    if emailAzienda['bcc'] == None:
        email = EmailMessage(subject, text_content, from_email, [to])
    # caso email con bcc
    elif emailAzienda.bcc2 == None:
        bcc_addresses = [emailAzienda.bcc]
        email = EmailMessage(subject, text_content,
                             from_email, [to], bcc=bcc_addresses)
    # caso email con due bcc
    else:
        bcc_addresses = [emailAzienda.bcc, emailAzienda.bcc2]
        email = EmailMessage(subject, text_content,
                             from_email, [to], bcc=bcc_addresses)
    email.attach_file(percorso)
    email.send()
    try:
        num_email_inviati = 2
        ritorno = True
    except:
        ritorno = False

    return ritorno
