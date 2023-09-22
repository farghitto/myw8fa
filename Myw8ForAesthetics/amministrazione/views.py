from django.shortcuts import render

# Create your views here.
def inviomail(request, tipo):
 
    return 0

def inviasms(chiave , id):

    
    user = 'infomyw8'
    password = 'WRfv24#$'

    # concatena le credenziali con il carattere ':'
    credentials = f"{user}:{password}"
    
    # codifica le credenziali in base64
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # crea l'header di autorizzazione con il valore base64
    authorization_header = f"Basic {encoded_credentials}"
    url = 'https://dashboard.wausms.com/Api/rest/message'

    # definisce gli header della richiesta
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': authorization_header
    }

    cellulare = cliente.cellulare
    # definisce i dati da inviare come corpo della richiesta
    data = {
        'to': ['39'+str(cellulare)],
        'text': 'Grazie di averci accordado la tua fiducia, il codice da comunicare è :' + str(codice),
        'from': 'W.T.A. MyW8'
    }

    # converte i dati in formato JSON
    json_data = json.dumps(data)

    # esegue la richiesta HTTP POST con gli header e i dati specificati
    response = requests.post(url, headers=headers, data=json_data)
    
    # stampa il codice di stato della risposta HTTP
    print(response.status_code)
    print(codice)
    # stampa il contenuto della risposta HTTP
    print(response.content)
    
    return response.status_code