from PyPDF2 import PdfWriter, PdfReader

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from datetime import date, datetime
import io
import os
import requests
import pdb

from django.shortcuts import get_object_or_404, redirect
from django.conf import settings


def moduloOrdine(request, id):
    
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #
    #can.setFillColorRGB(1,0,0) #choose your font colour
    can.setFont("Helvetica", 10)
    #
    #richiama cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    
    #richiama ordine
    url_backend = settings.BASE_URL + 'ordini/ordini/ultimo/'+str(id)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    
    if response.status_code == 200:
        ordini = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    
    #dettagli ordine
    url_backend = settings.BASE_URL + 'ordini/dettagli/'+str(ordini['id'])
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    
    if response.status_code == 200:
        dettagli = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    
    
    
    #anagrafica
    #prima riga x,y partendo dall'angolo in basso a sinistra
    can.drawString(33,713, cliente['cognome'])
    can.drawString(310,713, cliente['nome'])

    # # riga 2 - 23y
    can.drawString(33,690, cliente['citta_nascita'])
    
    data_originale = cliente['data_nascita']
    dt = datetime.strptime(data_originale, "%Y-%m-%d").strftime("%d-%m-%Y")
   

    can.drawString(310,690, dt )

    # # riga 3 - 23y
    can.drawString(33,667, cliente['citta'])
    can.drawString(310,667, cliente['cap'])

    # # riga 4 - 23y
    can.drawString(33,644, cliente['indirizzo'] )
    can.drawString(310,644, cliente['codice_fiscale'])

     # riga 5 - 23y
    can.drawString(33,621, cliente['cellulare'])
    can.drawString(310,621, cliente['email'])


    # dati cliente con partita iva
    if cliente['ragione_sociale'] is not None:
        # riga 1
        can.drawString(33,575, cliente['ragione_sociale'])
        can.drawString(310,575, cliente['sede'])
        # riga 2 - 23y
        can.drawString(33,552, cliente['indirizzo_sede'])
        can.drawString(310,552, cliente['cap_sede'])
        # riga 3 - 23y
        can.drawString(33,529,  cliente['telefono_sede'])
        can.drawString(310,529, cliente['email_sede'])
        # riga 4 - 23y
        can.drawString(33,506,  cliente['partita_iva'])
        can.drawString(310,506, cliente['codice_univoco'])

    # dati cliente con beneficiario
    if cliente['beneficiario_nome'] is not None:
        # riga 1
        can.drawString(33,460, cliente['beneficiario_cognome'])
        can.drawString(310,460, cliente['beneficiario_codice_fiscale'])
        # riga 2 - 23y
        can.drawString(33,437, cliente['beneficiario_nome'])
        can.drawString(310,437, cliente['beneficiario_cellulare'])

    #consulente
    can.drawString(33,387, cliente['consulente.nome'] + " " + cliente['consulente.cognome'])
    can.drawString(310,387, cliente['consulente.cellulare'])
 
    """   # # dati Biometrici riga 1
    # can.drawString(33,341,str(anag.peso_attuale))
    # can.drawString(220,341,strcliente['altezza'])
    # can.drawString(405,341,str(cliente['peso_desiderato'])
    #
    # # dati Biometrici riga 2 - 23y
    # can.drawString(33,318,str(anag.bmi_calcolato))
    # can.drawString(220,318,str(anag.peso_obiettivo))
    # can.drawString(405,318,cliente['note'])
    """
    # Programma
    can.drawString(33,272,dettagli['nome_programma'])
    can.drawString(220,272,str(dettagli['durata_programma']))
    can.drawString(405,272,str(dettagli['importo']))

    # tipologia pagamento riga 1
    can.drawString(170,226,str(dettagli['importo']))

    # tipologia pagamento riga 2 - 23y
    if dettagli['tipo'] == 'Rateale':
        can.drawString(170,203,str(dettagli['importo_acconto']))
        can.drawString(310,203,str(dettagli['numero_rate']))
        can.drawString(447,203,str(dettagli['importo_rate']))

    # tipologia pagamento riga 3 - 23y
    #if modalita == 'Finanziato':
     #   can.drawString(170,203,str(modalita_rateale['importo_acconto']))
      #  can.drawString(310,203,str(modalita_rateale['numero_rate']))
       # can.drawString(447,203,str(modalita_rateale['importo_rata']))
    #causale
    can.drawString(400,134,str(cliente['nome'] + " " + cliente['cognome'] + " " + dettagli['nome_programma']))
    #nota per indirizzo di spedizione diverso da indirizzo
    


    #data e luogo
    can.drawString(170,53, cliente['citta'])
    dt = date.today()
    sd = str(dt.day)
    if len(sd) == 1:
        sd = '0' + sd
    can.drawString(43,53, sd)
    sd = str(dt.month)
    if len(sd) == 1:
        sd = '0' + sd
    can.drawString(73,53, sd)
    sd = str(dt.year)
    can.drawString(103,53, sd)


    can.save()
    ###### pagina due
    packet1 = io.BytesIO()
    # create a new PDF with Reportlab
    can1 = canvas.Canvas(packet1, pagesize=letter)
    #
    #can.setFillColorRGB(1,0,0) #choose your font colour
    can1.setFont("Helvetica", 10)
    #

    #data e luogo
    can1.drawString(170,63, cliente['citta'])
    dt = date.today()
    sd = str(dt.day)
    if len(sd) == 1:
        sd = '0' + sd
    can1.drawString(43,63, sd)
    sd = str(dt.month)
    if len(sd) == 1:
        sd = '0' + sd
    can1.drawString(73,63, sd)
    sd = str(dt.year)
    can1.drawString(103,63, sd)



    can1.save()

  
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    # read your existing PDF

    existing_pdf = PdfReader(open("static/static_file/ordine.pdf", "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    packet1.seek(0)
    new_pdf = PdfReader(packet1)
    page = existing_pdf.pages[1]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    cartella_destinazione = 'pdf/' + str(cliente['codice_fiscale'])

    # Verifica e crea la cartella se non esiste
    if not os.path.exists(cartella_destinazione):
        try:
            os.makedirs(cartella_destinazione)
            
        except OSError as e:
            print(
                f"Errore durante la creazione della cartella '{cartella_destinazione}': {e}")

    ordine = ordini['numero_ordine']
    # Ora puoi aprire il file PDF nella cartella specificata
    nome_file_pdf = f"ordine-{ordine}.pdf"
    percorso_completo_pdf = os.path.join(cartella_destinazione, nome_file_pdf)

    outputStream = open(percorso_completo_pdf, "wb")
    output.write(outputStream)
    outputStream.close()
    pdb.set_trace()
    return percorso_completo_pdf