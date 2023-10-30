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
    # can.setFillColorRGB(1,0,0) #choose your font colour
    can.setFont("Helvetica", 10)
    #
    # richiama dati
    url_backend = settings.BASE_URL + 'ordini/datiordinepdf/'+str(id)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        dati = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # anagrafica
    # prima riga x,y partendo dall'angolo in basso a sinistra
    can.drawString(33, 713, dati['cliente']['cognome'])
    can.drawString(310, 713, dati['cliente']['nome'])

    # # riga 2 - 23y
    can.drawString(33, 690, dati['cliente']['citta_nascita'])

    data_originale = dati['cliente']['data_nascita']
    dt = datetime.strptime(data_originale, "%Y-%m-%d").strftime("%d-%m-%Y")

    can.drawString(310, 690, dt)

    # # riga 3 - 23y
    can.drawString(33, 667, dati['cliente']['citta'])
    can.drawString(310, 667, dati['cliente']['cap'])

    # # riga 4 - 23y
    can.drawString(33, 644, dati['cliente']['indirizzo'])
    can.drawString(310, 644, dati['cliente']['codice_fiscale'])

    # riga 5 - 23y
    can.drawString(33, 621, dati['cliente']['cellulare'])
    can.drawString(310, 621, dati['cliente']['email'])

    # dati cliente con partita iva
    if dati['cliente']['ragione_sociale'] is not None:
        # riga 1
        can.drawString(33, 575, dati['cliente']['ragione_sociale'])
        can.drawString(310, 575, dati['cliente']['sede'])
        # riga 2 - 23y
        can.drawString(33, 552, dati['cliente']['indirizzo_sede'])
        can.drawString(310, 552, dati['cliente']['cap_sede'])
        # riga 3 - 23y
        can.drawString(33, 529,  dati['cliente']['telefono_sede'])
        can.drawString(310, 529, dati['cliente']['email_sede'])
        # riga 4 - 23y
        can.drawString(33, 506,  dati['cliente']['partita_iva'])
        can.drawString(310, 506, dati['cliente']['codice_univoco'])

    # dati cliente con beneficiario
    if dati['cliente']['beneficiario_nome'] is not None:
        # riga 1
        can.drawString(33, 460, dati['cliente']['beneficiario_cognome'])
        can.drawString(310, 460, dati['cliente']
                       ['beneficiario_codice_fiscale'])
        # riga 2 - 23y
        can.drawString(33, 437, dati['cliente']['beneficiario_nome'])
        can.drawString(310, 437, dati['cliente']['beneficiario_cellulare'])

    # consulente
    can.drawString(
        33, 387, dati['consulente']['nome'] + " " + dati['consulente']['cognome'])
    can.drawString(310, 387, dati['consulente']['cellulare'])

    """   # # dati Biometrici riga 1
    # can.drawString(33,341,str(anag.peso_attuale))
    # can.drawString(220,341,str(dati['cliente']['altezza'])
    # can.drawString(405,341,str(dati['cliente']['peso_desiderato'])
    #
    # # dati Biometrici riga 2 - 23y
    # can.drawString(33,318,str(anag.bmi_calcolato))
    # can.drawString(220,318,str(anag.peso_obiettivo))
    # can.drawString(405,318,dati['cliente']['note'])
    """
    # Programma
    can.drawString(33, 272, dati['nome_programma'])
    can.drawString(220, 272, str(dati['durata_programma']))
    can.drawString(405, 272, str(dati['importo_programma']))

    # tipologia pagamento riga 1
    can.drawString(170, 226, str(dati['importo_programma']))

    # tipologia pagamento riga 2 - 23y
    if dati['tipo'] == 'Rateale':
        can.drawString(170, 203, str(dati['importo_acconto']))
        can.drawString(310, 203, str(dati['numero_rate']))
        can.drawString(447, 203, str(dati['importo_rate']))

    # tipologia pagamento riga 3 - 23y
    # if modalita == 'Finanziato':
     #   can.drawString(170,203,str(modalita_rateale['importo_acconto']))
      #  can.drawString(310,203,str(modalita_rateale['numero_rate']))
       # can.drawString(447,203,str(modalita_rateale['importo_rata']))
    # causale
    can.drawString(400, 134, str(
        dati['cliente']['nome'] + " " + dati['cliente']['cognome'] + " " + dati['nome_programma']))
    # nota per indirizzo di spedizione diverso da indirizzo

    # data e luogo
    can.drawString(170, 53, dati['cliente']['citta'])
    dt = date.today()
    sd = str(dt.day)
    if len(sd) == 1:
        sd = '0' + sd
    can.drawString(43, 53, sd)
    sd = str(dt.month)
    if len(sd) == 1:
        sd = '0' + sd
    can.drawString(73, 53, sd)
    sd = str(dt.year)
    can.drawString(103, 53, sd)

    can.save()
    # pagina due
    packet1 = io.BytesIO()
    # create a new PDF with Reportlab
    can1 = canvas.Canvas(packet1, pagesize=letter)
    #
    # can.setFillColorRGB(1,0,0) #choose your font colour
    can1.setFont("Helvetica", 10)
    #

    # data e luogo
    can1.drawString(170, 63, dati['cliente']['citta'])
    dt = date.today()
    sd = str(dt.day)
    if len(sd) == 1:
        sd = '0' + sd
    can1.drawString(43, 63, sd)
    sd = str(dt.month)
    if len(sd) == 1:
        sd = '0' + sd
    can1.drawString(73, 63, sd)
    sd = str(dt.year)
    can1.drawString(103, 63, sd)

    can1.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    # read your existing PDF

    existing_pdf = PdfReader(open("static/static_file/ordine.pdf", "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    packet1.seek(0)
    new_pdf = PdfReader(packet1)
    page = existing_pdf.pages[1]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    cartella_destinazione = 'pdf/' + str(dati['cliente']['codice_fiscale'])

    # Verifica e crea la cartella se non esiste
    if not os.path.exists(cartella_destinazione):
        try:
            os.makedirs(cartella_destinazione)

        except OSError as e:
            print(
                f"Errore durante la creazione della cartella '{cartella_destinazione}': {e}")

    ordine = dati['numero_ordine'].replace('/', '-')
    nome_file_pdf = f"ordine-{ordine}.pdf"

    percorso_completo_pdf = os.path.join(cartella_destinazione, nome_file_pdf)

    outputStream = open(percorso_completo_pdf, "wb")
    output.write(outputStream)
    outputStream.close()

    return percorso_completo_pdf


def moduloOrdineFirmato(request, id):

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #
    # can.setFillColorRGB(1,0,0) #choose your font colour
    can.setFont("Helvetica", 10)
    #
    # richiama dati
    url_backend = settings.BASE_URL + 'ordini/datiordinepdf/'+str(id)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        dati = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    prima_parte_accordo = dati['numero_ordine'].split('/')[0]
    seconda_parte_accordo = dati['numero_ordine'].split('/')[1]

    can.drawString(516, 813, str(prima_parte_accordo))
    can.drawString(550, 813, str(seconda_parte_accordo))

    can.drawString(376, 63, str("firmato da " +
                   dati['cliente']['cognome'] + " " + dati['cliente']['nome']))
    can.drawString(376, 43, str(
        "con email inviata a  " + dati['cliente']['email']))
    can.drawString(376, 53, str(
        "in data  " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

    can.save()
    # pagina due
    packet1 = io.BytesIO()
    # create a new PDF with Reportlab
    can1 = canvas.Canvas(packet1, pagesize=letter)
    #
    # can.setFillColorRGB(1,0,0) #choose your font colour
    can1.setFont("Helvetica", 10)
    #

    can1.drawString(516, 813, str(prima_parte_accordo))
    can1.drawString(550, 813, str(seconda_parte_accordo))
    can1.drawString(376, 73, str(
        "firmato da " + dati['cliente']['cognome'] + " " + dati['cliente']['nome']))
    can1.drawString(376, 53, str(
        "con email inviata a  " + dati['cliente']['email']))
    can1.drawString(376, 63, str(
        "in data  " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

    can1.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    # read your existing PDF
    cartella_destinazione = 'pdf/' + str(dati['cliente']['codice_fiscale'])
    ordine = dati['numero_ordine'].replace('/', '-')
    nome_file_pdf = f"ordine-{ordine}.pdf"
    percorso_completo_pdf = os.path.join(cartella_destinazione, nome_file_pdf)

    existing_pdf = PdfReader(open(percorso_completo_pdf, "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    packet1.seek(0)
    new_pdf = PdfReader(packet1)
    page = existing_pdf.pages[1]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    nome_file_pdf_firmato = f"ordine_firmato-{ordine}.pdf"
    percorso_completo_pdf_firmato = os.path.join(
        cartella_destinazione, nome_file_pdf_firmato)
    # finally, write "output" to a real file
    outputStream = open(percorso_completo_pdf_firmato, "wb")
    output.write(outputStream)
    outputStream.close()

    return percorso_completo_pdf_firmato
