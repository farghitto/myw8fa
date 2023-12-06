from turtle import pd
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

from django.shortcuts import redirect
from django.conf import settings
from django.core.paginator import Paginator




def moduloDati (request, id):

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #
    #can.setFillColorRGB(1,0,0) #choose your font colour
    can.setFont("Helvetica", 10)
    #

    # richiama dati
    url_backend = settings.BASE_URL + 'cliente/datimoduloinfopdf/'+str(id)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        dati = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    
    
    ordine = dati['ordine']['numero_ordine']
    
    
    

    #anagrafica
    #prima riga x,y partendo dall'angolo in basso a sinistra
    can.drawString(250,735,  dati['cliente']['cognome'])

    # # riga 2 - 25y
    can.drawString(250,710,  dati['cliente']['nome'])

    # # riga 3 - 25y
    can.drawString(120,685,  dati['cliente']['codice_fiscale'])
    can.drawString(395,685, str(ordine))

    data_originale = dati['cliente']['data_nascita']
    dt = datetime.strptime(data_originale, "%Y-%m-%d").strftime("%d-%m-%Y")

    # # riga 4 - 25y
    can.drawString(25,660, str(dt))
    can.drawString(150,660, dati['cliente']['citta_nascita'])
    can.drawString(280,660, dati['cliente']['provincia_nascita'])
    can.drawString(402,660, dati['cliente']['stato_nascita'])

    # # riga 5 - 25y
    can.drawString(25,635, str(dati['cliente']['indirizzo']) + ' ' + str(dati['cliente']['numero_civico']))
    can.drawString(150,635, dati['cliente']['citta'])
    can.drawString(280,635, dati['cliente']['provincia_residenza'])
    can.drawString(402,635, dati['cliente']['stato_residenza'])

    # # riga 6 - 25y
    can.drawString(25,611,  dati['cliente']['cellulare'])
    can.drawString(110,611, dati['cliente']['email'])
    can.drawString(235,611, dati['cliente_data']['professione'])
    can.drawString(358,611, dati['cliente']['sesso'])
    can.drawString(402,611,  dati['cliente_data']['stato_civile'])
    can.drawString(465,611, dati['cliente_data']['maggiorenne'])

    if dati['cliente']['sesso'] == 'F':
        # # riga 7
        can.drawString(90,570, dati['cliente_data']['struttura_fisica'])
        # # riga 8
        can.drawString(90,530, dati['cliente_data']['struttura_desiderata'])

    else:
        
        struttuta = dati['cliente_data']['struttura_fisica']
        struttura_des = dati['cliente_data']['struttura_desiderata']
        struttuta = struttuta.replace("A", "F")
        struttuta = struttuta.replace("B", "G")
        struttuta = struttuta.replace("C", "H")
        struttuta = struttuta.replace("D", "I")
        struttuta = struttuta.replace("E", "L")
        struttura_des = struttura_des.replace("A", "F")
        struttura_des = struttura_des.replace("B", "G")
        struttura_des = struttura_des.replace("C", "H")
        struttura_des = struttura_des.replace("D", "I")
        struttura_des = struttura_des.replace("E", "L")

        # # riga 7
        can.drawString(90,570, struttuta)
        # # riga 8
        can.drawString(90,530, struttura_des)

    # # riga 9
    can.drawString(25,486, dati['cliente_data']['peso_attuale'])
    can.drawString(100,486, dati['cliente_data']['altezza'])
    can.drawString(170,486, dati['cliente_data']['bmi'])
    can.drawString(225,486, dati['cliente_data']['stato_attuale'])
    can.drawString(307,486, dati['cliente_data']['peso_ottimale'])
    can.drawString(370,486, dati['cliente_data']['scostamento_peso'])
    can.drawString(452,486, dati['cliente_data']['peso_desiderato'])

    # # riga 10 - 25y
    can.drawString(25,461, dati['cliente_data']['pressione_arteriosa'])
    can.drawString(100,461, dati['cliente_data']['diabete'])
    if dati['cliente_data']['tipo_diabete'] != None:
        can.drawString(148,461, dati['cliente_data']['tipo_diabete'])
    if dati['cliente']['sesso'] == 'F':
        can.drawString(205,461, dati['cliente_data']['menopausa'])
        can.drawString(265,461, dati['cliente_data']['gravidanza'])
        if dati['cliente_data']['mesi_gravidanza'] != None:
            can.drawString(330,461, dati['cliente_data']['mesi_gravidanza'])
    can.drawString(430,461, dati['cliente_data']['rapporto_corpo'])
    can.drawString(480,461, dati['cliente_data']['droghe'])

    # # riga 11 - 25y
    can.drawString(25,438, dati['cliente_data']['allergie'])
    if dati['cliente_data']['allergie_elenco'] != None:
        can.drawString(100,438, dati['cliente_data']['allergie_elenco'])

    # # riga 12 - 25y
    can.drawString(25,414, dati['cliente_data']['farmaci'])
    if dati['cliente_data']['farmaci_elenco'] != None:
        can.drawString(100,414, dati['cliente_data']['farmaci_elenco'])


    # # riga 13 - 25y
    can.drawString(25,390, dati['cliente_data']['sport'])
    if dati['cliente_data']['sport_praticato'] != None:
        can.drawString(100,390, dati['cliente_data']['sport_praticato'])
        can.drawString(239,390, dati['cliente_data']['sport_praticato_giorni'])
    can.drawString(322,390, dati['cliente_data']['gruppo_sanguigno'])
    can.drawString(407,390, dati['cliente_data']['insonnia'])
    can.drawString(463,390, dati['cliente_data']['stitichezza'])

    # # riga 14 - 25y
    can.drawString(25,366, dati['cliente_data']['fumo'])
    if dati['cliente_data']['numero_sigarette'] != None:
        can.drawString(60,366, dati['cliente_data']['numero_sigarette'])
        can.drawString(248,366, dati['cliente_data']['delta_numero_sigarette'])
    can.drawString(297,366, dati['cliente_data']['fame_nervosa'])
    can.drawString(370,366, dati['cliente_data']['gengive'])
    can.drawString(450,366, dati['cliente_data']['tatuaggi'])

    # # riga 15 - 25y
    can.drawString(25,342, dati['cliente_data']['bevi_acqua'])
    can.drawString(100,342, dati['cliente_data']['litri_acqua'])
    can.drawString(200,342, dati['cliente_data']['filosofia_alimentare'])
    can.drawString(290,342, dati['cliente_data']['maiale'])
    can.drawString(357,342, dati['cliente_data']['figli'])
    if dati['cliente_data']['numero_figli'] != None:

        can.drawString(395,342, dati['cliente_data']['numero_figli'])
        can.drawString(430,342, dati['cliente_data']['pasto_condiviso'])

    alimenti = dati['cliente_data']['alimenti_preferiti']
    gusti = dati['cliente_data'] ['gusti_preferiti']
    # # riga 16 - 25y
    if 'Caffè' in alimenti:
        can.drawString(25,318, 'X')

    if 'Pane' in alimenti:
        can.drawString(64,318, 'X')

    if 'Verdure' in alimenti:
        can.drawString(96,318, 'X')

    if 'Carne' in alimenti:
        can.drawString(129,318, 'X')

    if 'Cereali' in alimenti:
        can.drawString(163,318, 'X')

    if 'Cioccolata' in alimenti:
        can.drawString(197,317, 'X')

    if 'Legumi' in alimenti:
        can.drawString(241,317, 'X')

    if 'Piccante' in gusti:
        can.drawString(409,318, 'X')

    if 'Dolce' in gusti:
        can.drawString(446,318, 'X')

    if 'Salato' in gusti:
        can.drawString(482,318, 'X')

    # # riga 17 - 25y
    if 'Alcolici' in alimenti:
        can.drawString(25,306, 'X')

    if 'Pasta' in alimenti:
        can.drawString(64,306, 'X')

    if 'Frutta' in alimenti:
        can.drawString(96,306, 'X')

    if 'Pesce' in alimenti:
        can.drawString(129,306, 'X')

    if 'Dolci' in alimenti:
        can.drawString(163,306, 'X')

    if 'Pizza' in alimenti:
        can.drawString(197,305, 'X')

    if 'Latticini' in alimenti:
        can.drawString(241,305, 'X')

    if 'Amaro' in gusti:
        can.drawString(409,306, 'X')

    if 'Aspro' in gusti:
        can.drawString(446,306, 'X')

    if 'Insipido' in gusti:
        can.drawString(482,306, 'X')

    patologie = dati['lista_patologie']
    
    # # riga 1 patologie
    if 'Acidita' in patologie:
        can.drawString(28,281, 'X')

    if 'Calcolosi biliare' in patologie:
        can.drawString(91,281, 'X')

    if 'Dismenorrea' in patologie:
        can.drawString(179,281, 'X')

    if 'Ernia latale' in patologie:
        can.drawString(270,281, 'X')

    if 'Ipoglicemia' in patologie:
        can.drawString(346,281, 'X')

    if 'Prostatite' in patologie:
        can.drawString(418,281, 'X')

    # # riga 2 patologie
    if 'Acne' in patologie:
        can.drawString(28,274, 'X')

    if 'Cancro' in patologie:
        can.drawString(91,274, 'X')

    if 'Disturbi del comportamento' in patologie:
        can.drawString(179,274, 'X')

    if 'Fibroma' in patologie:
        can.drawString(270,274, 'X')

    if 'Ipotiroidismo' in patologie:
        can.drawString(346,274, 'X')

    if 'Prurito continuo' in patologie:
        can.drawString(418,274, 'X')

    # # riga 3 patologie
    if 'Affaticamento' in patologie:
        can.drawString(28,267, 'X')

    if 'Candidosi' in patologie:
        can.drawString(91,267, 'X')

    if 'Disturmi intestinali' in patologie:
        can.drawString(179,267, 'X')

    if 'Gastrite/Ulcera gastrica' in patologie:
        can.drawString(270,267, 'X')

    if 'Mal di testa' in patologie:
        can.drawString(346,267, 'X')

    if 'Psoriasi' in patologie:
        can.drawString(418,267, 'X')

    # # riga 4 patologie
    if 'Afta' in patologie:
        can.drawString(28,260, 'X')

    if 'Celiachia' in patologie:
        can.drawString(91,260, 'X')

    if 'Disturbi polmonari' in patologie:
        can.drawString(179,260, 'X')

    if 'Gotta' in patologie:
        can.drawString(270,260, 'X')

    if 'Meteorismo' in patologie:
        can.drawString(346,260, 'X')

    if 'Reumastismo' in patologie:
        can.drawString(418,260, 'X')

    # # riga 5 patologie
    if 'Alitosi' in patologie:
        can.drawString(28,251, 'X')

    if 'Cisti ovariche' in patologie:
        can.drawString(91,251, 'X')

    if 'Diverticolite' in patologie:
        can.drawString(179,251, 'X')

    if 'Infezioni ricorrenti' in patologie:
        can.drawString(270,251, 'X')

    if 'Nevralgia' in patologie:
        can.drawString(346,251, 'X')

    if 'Sclerosi multipla' in patologie:
        can.drawString(418,251, 'X')

    # # riga 6 patologie
    if 'Anemia' in patologie:
        can.drawString(28,243, 'X')

    if 'Colesterolo alto' in patologie:
        can.drawString(91,243, 'X')

    if 'Dolori Addominali' in patologie:
        can.drawString(179,243, 'X')

    if 'Inappetenza' in patologie:
        can.drawString(270,243, 'X')

    if 'Obesità' in patologie:
        can.drawString(346,243, 'X')

    if 'Talassemia' in patologie:
        can.drawString(418,243, 'X')

    # # riga 7 patologie
    if 'Arteriosclerosi' in patologie:
        can.drawString(28,235, 'X')

    if 'Colite' in patologie:
        can.drawString(91,235, 'X')

    if 'Emicrania' in patologie:
        can.drawString(179,235, 'X')

    if 'Intolleranza al lattosio' in patologie:
        can.drawString(270,235, 'X')

    if 'Osteoporosi' in patologie:
        can.drawString(346,235, 'X')

    if 'Trigliceridi alti' in patologie:
        can.drawString(418,235, 'X')

    # # riga 8 patologie
    if 'Artrosi' in patologie:
        can.drawString(28,228, 'X')

    if 'Depressione' in patologie:
        can.drawString(91,228, 'X')

    if 'Emorroidi' in patologie:
        can.drawString(179,228, 'X')

    if 'Iperglicemia' in patologie:
        can.drawString(270,228, 'X')

    if 'Pancreatite' in patologie:
        can.drawString(346,228, 'X')

    if 'Varici' in patologie:
        can.drawString(418,228, 'X')

    # # riga 9 patologie
    if 'Autismo' in patologie:
        can.drawString(28,220, 'X')

    if 'Diarrea' in patologie:
        can.drawString(91,220, 'X')

    if 'Epilessia' in patologie:
        can.drawString(179,220, 'X')

    if 'Ipertiroidismo' in patologie:
        can.drawString(270,220, 'X')

    if 'Paradontite' in patologie:
        can.drawString(346,220, 'X')

    if 'Vertigini' in patologie:
        can.drawString(418,220, 'X')


    # # riga 19 - 25y
    can.drawString(25,198, dati['cliente_data']['problemi_cardiaci'])
    if dati['cliente_data']['problem_cardiaci_tipo'] != None:

        can.drawString(125,198, dati['cliente_data']['problem_cardiaci_tipo'])

    # # riga 20
    can.drawString(25,174, dati['cliente_data']['sicura'])
    can.drawString(89,174, dati['cliente_data']['felice'])
    can.drawString(138,174, dati['cliente_data']['stress'])
    can.drawString(190,174, dati['cliente_data']['paure'])
    can.drawString(250,174, dati['cliente_data']['lutti'])
    can.drawString(312,174, dati['cliente_data']['incubi'])
    can.drawString(363,174, dati['cliente_data']['stanco'])
    can.drawString(420,174, dati['cliente_data']['rabbia'])
    can.drawString(475,174, dati['cliente_data']['sfogo'])

    # # riga 21
    can.drawString(25,151, dati['cliente_data']['colpa'])
    can.drawString(89,151, dati['cliente_data']['piangi'])
    can.drawString(130,151, dati['cliente_data']['carattere1'])
    can.drawString(190,151, dati['cliente_data']['carattere2'])
    can.drawString(250,151, dati['cliente_data']['carattere3'])
    can.drawString(318,151, dati['cliente_data']['determinato'])
    can.drawString(415,151, dati['cliente_data']['amici_dieta'])

    # # riga 22
    if dati['cliente_data']['note'] != None:

        can.drawString(25,126, dati['cliente_data']['note'])


    # # riga 23
    can.drawString(296,58, 'X')

    # # riga 24
    can.drawString(296,45, 'X')

    # # riga 25
    can.drawString(296,32, 'X')

    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open("static/static_file/modulo_informazioni.pdf", "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)


    # finally, write "output" to a real file
   
    
    cartella_destinazione = 'pdf/' + str(dati['cliente']['codice_fiscale'])

    # Verifica e crea la cartella se non esiste
    if not os.path.exists(cartella_destinazione):
        try:
            os.makedirs(cartella_destinazione)

        except OSError as e:
            print(
                f"Errore durante la creazione della cartella '{cartella_destinazione}': {e}")

    
    nome_file_pdf = f"modulodati-{dati['cliente']['cognome']}.pdf"

    percorso_completo_pdf = os.path.join(cartella_destinazione, nome_file_pdf)

    outputStream = open(percorso_completo_pdf, "wb")
    output.write(outputStream)
    outputStream.close()
    
    
    indirizzo_allegati = {
        'file_modulo_dati' : percorso_completo_pdf,
    }  
    
    return indirizzo_allegati


def moduloAlimenti (request, id):
    
    


    width, height = A4
    output = PdfWriter()

     # richiama dati
    url_backend = settings.BASE_URL + 'cliente/datimoduloalimentipdf/'+str(id)
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        dati = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)
    
    url_backend = settings.BASE_URL + 'cliente/listaalimenti/'
    headers = {
        "Authorization": f"Token {request.session['auth_token']}"
    }
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        alimenti = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)


    #anagrafica
    data=[]
    classealimento = ''

    #per tutti gli alimenti presenti nella lista
    for alimento in alimenti:     
        #se l'alimento selezionato a una classe alimebnto diversa da quella che stiamo considerando prendo la sua classe come titolo
        #e la cambio, altrimenti rimango con quella che ho
        if alimento['classe_alimenti'] != classealimento:

            riga = [str(alimento['classe_alimenti']).upper(),' ']
            data.append(riga)
            classealimento = alimento['classe_alimenti']

        #se l'alimento è stato scartato esso sara nella lista degli alimenti del cliente
        
        # contiene tutti gli elementi scartati dal cliente
        gusti_alimenti = dati['gusti_alimenti']
        
        alimento_da_verificare =  alimento['id']

        # Verifica se c'è un elemento con 'alimento' uguale a 28
        alimento_presente = next((gusto for gusto in gusti_alimenti if gusto['alimento'] == alimento_da_verificare), None)
        if alimento_presente:
            #vediamo se è allergico o no
            if alimento_presente['allergia']:
                riga = [str(alimento['nome']), str('A')]
            else:
                riga = [str(alimento['nome']), str('N')]
            data.append(riga)
        else:
            #se non è presente è gradito
            riga = [str(alimento['nome']), 'G']
            data.append(riga)


    righe_tabella = []
    riga_appoggio = []
    datalen = len(data)
    iterazioni = 1

    for dato in data:


        if dato[1] == ' ' :

            if riga_appoggio:

                righe_tabella.append(riga_appoggio[:])
                riga_appoggio.clear()

            dato.append(' ')
            dato.append(' ')
            dato.append(' ')
            dato.append(' ')
            righe_tabella.append(dato)

        else:
            if len(riga_appoggio) <= 4:
                riga_appoggio.append(dato[0])
                riga_appoggio.append(dato[1])
            else:

                righe_tabella.append(riga_appoggio[:])
                riga_appoggio.clear()
                riga_appoggio.append(dato[0])
                riga_appoggio.append(dato[1])

        if iterazioni == datalen:
            righe_tabella.append(riga_appoggio[:])

        iterazioni = iterazioni + 1

    prima_pagina_intevallo = 0
    ultima_pagina_intervallo = 0
    cont = 0
    for riga in righe_tabella:

        if cont <= 32:
             if riga[1] == ' ':
                 prima_pagina_intevallo = cont - 2


        if cont > 32 and cont <70:

            if riga[1] == ' ':

                ultima_pagina_intervallo = cont
        cont = cont +1

    numero_righe_tabella = len(righe_tabella)
    numero_righe_pagine_interne = numero_righe_tabella - prima_pagina_intevallo - (numero_righe_tabella - ultima_pagina_intervallo)
    dati_paginator=[]
    dati_paginator.append(righe_tabella[0:prima_pagina_intevallo])
    dati_paginator.append(righe_tabella[(prima_pagina_intevallo):(prima_pagina_intevallo + numero_righe_pagine_interne)])
    dati_paginator.append(righe_tabella[(prima_pagina_intevallo + numero_righe_pagine_interne ):])


    pag_alimento = Paginator(dati_paginator, 1)


    for i in pag_alimento.page_range:

        page = pag_alimento.get_page(i)

        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=A4)
        #

        can.setFont("Helvetica", 12)
        # prima pagina
        if not page.has_previous():

            #prima riga x,y partendo dall'angolo in basso a sinistra
            can.drawString(110,755, dati['cliente']['nome'])
            can.drawString(368,755, dati['cliente']['cognome'])

            x = 30

            lista_stili = [('INNERGRID', (0,0), (-1,-1), 0.25, colors.red),
            ('BOX', (0,0), (-1,-1), 0.25, colors.red)]
            for idx, riga in enumerate(dati_paginator[i-1]):


                if riga[1] == ' ':
                    lista_stili.append(('TEXTCOLOR',(0,idx),(1,idx),colors.white))
                    lista_stili.append(('ALIGN',(0,idx),(1,idx),'CENTER'))
                    lista_stili.append(('BACKGROUND',(0,idx),(5,idx),colors.red))
                    lista_stili.append(('SPAN',(0,idx),(5,idx)))



            tabella = Table(dati_paginator[i-1], colWidths=(140,20,140,20,140,20))
            tabella.setStyle(TableStyle(lista_stili))

            dimensioni_tab = tabella.wrapOn(can, width, height)
            y_dinamico = 640 - dimensioni_tab[1]
            tabella.drawOn(can, x,y_dinamico)



            can.showPage()
            can.save()
            packet.seek(0)

            new_pdf = PdfReader(packet)
            # read your existing PDF
            existing_pdf = PdfReader(open("static\static_file\modulo_alimenti.pdf", "rb"))

            # add the "watermark" (which is the new pdf) on the existing page
            pagina = existing_pdf.pages[0]
            pagina.merge_page(new_pdf.pages[0])
            output.add_page(pagina)

        #--------------------------------------------------------------
        #ultima pagina
        elif not page.has_next():

            can.setFont("Helvetica", 10)

            x = 30


            lista_stili = [('INNERGRID', (0,0), (-1,-1), 0.25, colors.red),
            ('BOX', (0,0), (-1,-1), 0.25, colors.red)]
            for idx, riga in enumerate(dati_paginator[i-1]):


                if riga[1] == ' ':
                    lista_stili.append(('TEXTCOLOR',(0,idx),(1,idx),colors.white))
                    lista_stili.append(('ALIGN',(0,idx),(1,idx),'CENTER'))
                    lista_stili.append(('BACKGROUND',(0,idx),(5,idx),colors.red))
                    lista_stili.append(('SPAN',(0,idx),(5,idx)))



            tabella = Table(dati_paginator[i-1], colWidths=(140,20,140,20,140,20))
            tabella.setStyle(TableStyle(lista_stili))

            dimensioni_tab = tabella.wrapOn(can, width, height)
            y_dinamico = 750 - dimensioni_tab[1]
            tabella.drawOn(can, x,y_dinamico)

            #legeenda tabella
            can.drawString(100,310, 'G = GRADITO       A = ALLERGIA       N = NON GRADITO')

              #privacy
            can.drawString(292,86, 'X')
            can.drawString(292,73, 'X')
            can.drawString(292,55, 'X')


            can.showPage()
            can.save()
            packet.seek(1)

            new_pdf = PdfReader(packet)
            # read your existing PDF
            existing_pdf = PdfReader(open("static\static_file\modulo_alimenti.pdf", "rb"))

            # add the "watermark" (which is the new pdf) on the existing page
            pagina = existing_pdf.pages[2]
            
            pagina.merge_page(new_pdf.pages[0])
            output.add_page(pagina)

        else:
                #--------------------------------------------------------------
                # altre pagine

                x = 30


                lista_stili = [('INNERGRID', (0,0), (-1,-1), 0.25, colors.red),
                ('BOX', (0,0), (-1,-1), 0.25, colors.red)]
                for idx, riga in enumerate(dati_paginator[i-1]):


                    if riga[1] == ' ':
                        lista_stili.append(('TEXTCOLOR',(0,idx),(1,idx),colors.white))
                        lista_stili.append(('ALIGN',(0,idx),(1,idx),'CENTER'))
                        lista_stili.append(('BACKGROUND',(0,idx),(5,idx),colors.red))
                        lista_stili.append(('SPAN',(0,idx),(5,idx)))



                tabella = Table(dati_paginator[i-1], colWidths=(140,20,140,20,140,20))
                tabella.setStyle(TableStyle(lista_stili))

                dimensioni_tab = tabella.wrapOn(can, width, height)
                y_dinamico = 750 - dimensioni_tab[1]
                tabella.drawOn(can, x,y_dinamico)



                can.showPage()
                can.save()
                packet.seek(2)

                new_pdf = PdfReader(packet)
                # read your existing PDF
                existing_pdf = PdfReader(open("static\static_file\modulo_alimenti.pdf", "rb"))

                # add the "watermark" (which is the new pdf) on the existing page
                pagina = existing_pdf.pages[1]
                pagina.merge_page(new_pdf.pages[0])
                output.add_page(pagina)


    
    
    cartella_destinazione = 'pdf/' + str(dati['cliente']['codice_fiscale'])

    # Verifica e crea la cartella se non esiste
    if not os.path.exists(cartella_destinazione):
        try:
            os.makedirs(cartella_destinazione)

        except OSError as e:
            print(
                f"Errore durante la creazione della cartella '{cartella_destinazione}': {e}")

    
    nome_file_pdf = f"moduloalimenti-{dati['cliente']['cognome']}.pdf"

    percorso_completo_pdf = os.path.join(cartella_destinazione, nome_file_pdf)

    outputStream = open(percorso_completo_pdf, "wb")
    output.write(outputStream)
    outputStream.close()
    
    
    indirizzo_allegati = {
        'file_modulo_alimenti' : percorso_completo_pdf,
    }  
    
    return indirizzo_allegati


   