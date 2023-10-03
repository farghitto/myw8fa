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


#
# solo firmato

def ModuloPersonal(request, id):

    # richiamare misure
    url_backend = settings.BASE_URL + 'cliente/misure/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        misure = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    # richiamare cliente
    url_backend = settings.BASE_URL + 'cliente/clienti/'+str(id)+'/'
    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        cliente = response.json()
    elif response.status_code >= 400:
        return redirect('erroreserver', status_code=response.status_code, text=response.text)

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    #
    # can.setFillColorRGB(1,0,0) #choose your font colour
    can.setFont("Helvetica", 10)

    datipersonal = misure
    # inserimento dati attuali
    primamisura = datipersonal[0]
    # prima misura inserita nel sistema
    ultimamisura = datipersonal[-1]

    if primamisura == ultimamisura:
        primamisurazione = True
    else:
        primamisurazione = False
        # ultimo inserimento prima dell'attuale
        penultimamisura = datipersonal[-2]

    # riga1
    can.drawString(100, 676, (str(cliente['nome'])))
    can.drawString(350, 676, (str(cliente['cognome'])))

    # riga 2
    can.drawString(90, 659, (str(cliente['cellulare'])))
    can.drawString(250, 659, (str(cliente['email'])))

    # riga 3
    formato = "%Y-%m-%d"
    data_di_nascita = datetime.strptime(
        cliente['data_nascita'], formato)
    data_corrente = date.today()
    eta = data_corrente.year - data_di_nascita.year - \
        ((data_corrente.month, data_corrente.day) <
         (data_di_nascita.month, data_di_nascita.day))
    can.drawString(70, 641, (str(eta)))
    can.drawString(170, 641, (str(cliente['altezza'])))
    can.drawString(265, 641, (str(cliente['sesso'])))

    # riga4
    can.drawRightString(265, 595, (str(round(primamisura['peso'], 2))))
    if primamisurazione:
        can.drawRightString(308, 595, ('--'))
        can.drawRightString(358, 595, ('--'))
        can.drawRightString(408, 595, ('--'))
    else:
        can.drawRightString(315, 595, (str(round(penultimamisura['peso'], 2))))
        can.drawRightString(
            365, 595, (str(round(primamisura['peso']-penultimamisura['peso'], 2))))
        can.drawRightString(
            415, 595, (str(round(primamisura['peso']-ultimamisura['peso'], 2))))

    # riga5
    can.drawRightString(265, 576, (str(round(primamisura['bmi'], 2))))
    if primamisurazione:
        can.drawRightString(308, 576, ('--'))
        can.drawRightString(358, 576, ('--'))
        can.drawRightString(408, 576, ('--'))
    else:
        can.drawRightString(315, 576, (str(round(primamisura['bmi'], 2))))
        can.drawRightString(
            365, 576, (str(round(primamisura['bmi']-penultimamisura['bmi'], 2))))
        can.drawRightString(
            415, 576, (str(round(primamisura['bmi']-ultimamisura['bmi'], 2))))

    # riga6
    # grasso corporeo non è obbligatorio! quidi se non è inserita la misurazione
    # la riga non è visualizzata, se è inserita ma non c'è la penultima è visibile
    # il confornto con il primo se esiste altrimenti lo inserisco come primo
    import pdb
    pdb.set_trace()
    if primamisura['grasso_corporeo']:
        can.drawRightString(
            265, 557, (str(round(primamisura['grasso_corporeo'], 2))))
        if primamisurazione:
            can.drawRightString(308, 559, ('--'))
            can.drawRightString(358, 559, ('--'))
            can.drawRightString(408, 559, ('--'))
        else:
            if ultimamisura['grasso_corporeo']:
                can.drawRightString(415, 557, (str(
                    round(primamisura['grasso_corporeo']-ultimamisura['grasso_corporeo'], 2))))
            # da sistemare else:
            #     registraprimamisura = get_object_or_404(
            #         PersonalCheckUpCliente, pk=ultimamisura.pk)
            #     registraprimamisura['grasso_corporeo'] = round(
            #         primamisura['grasso_corporeo'], 2)
            #     registraprimamisura.save()
            #     can.drawRightString(415, 557, (str(
            #         round(primamisura['grasso_corporeo']-registraprimamisura['grasso_corporeo'], 2))))

            if penultimamisura['grasso_corporeo']:
                can.drawRightString(
                    315, 557, (str(round(penultimamisura['grasso_corporeo'], 2))))
                can.drawRightString(365, 557, (str(
                    round(primamisura['grasso_corporeo']-penultimamisura['grasso_corporeo'], 2))))
            else:
                can.drawRightString(308, 559, ('--'))
                can.drawRightString(358, 559, ('--'))
    else:
        can.drawRightString(258, 559, ('--'))
        can.drawRightString(308, 559, ('--'))
        can.drawRightString(358, 559, ('--'))
        can.drawRightString(408, 559, ('--'))
    # riga7
    if primamisura['muscolatura']:
        can.drawRightString(
            265, 538, (str(round(primamisura['muscolatura'], 2))))
        if primamisurazione:
            can.drawRightString(308, 540, ('--'))
            can.drawRightString(358, 540, ('--'))
            can.drawRightString(408, 540, ('--'))
        else:
            if ultimamisura['muscolatura']:
                can.drawRightString(
                    415, 538, (str(round(primamisura['muscolatura']-ultimamisura['muscolatura'], 2))))
            # else:
            #     registraprimamisura = get_object_or_404(
            #         PersonalCheckUpCliente, pk=ultimamisura.pk)
            #     registraprimamisura['muscolatura'] = round(
            #         primamisura['muscolatura'], 2)
            #     registraprimamisura.save()
            #     can.drawRightString(415, 538, (str(
            #         round(primamisura['muscolatura']-registraprimamisura['muscolatura'], 2))))

            if penultimamisura['muscolatura']:
                can.drawRightString(
                    315, 538, (str(round(penultimamisura['muscolatura'], 2))))
                can.drawRightString(
                    365, 538, (str(round(primamisura['muscolatura']-penultimamisura['muscolatura'], 2))))
            else:
                can.drawRightString(308, 540, ('--'))
                can.drawRightString(358, 540, ('--'))
    else:
        can.drawRightString(258, 540, ('--'))
        can.drawRightString(308, 540, ('--'))
        can.drawRightString(358, 540, ('--'))
        can.drawRightString(408, 540, ('--'))
    # riga8
    if primamisura['metabolismo']:
        can.drawRightString(
            265, 519, (str(round(primamisura['metabolismo'], 2))))
        if primamisurazione:
            can.drawRightString(308, 521, ('--'))
            can.drawRightString(358, 521, ('--'))
            can.drawRightString(408, 521, ('--'))
        else:
            if ultimamisura['metabolismo']:
                can.drawRightString(
                    415, 519, (str(round(primamisura['metabolismo']-ultimamisura['metabolismo'], 2))))
            # else:
            #     registraprimamisura = get_object_or_404(
            #         PersonalCheckUpCliente, pk=ultimamisura.pk)
            #     registraprimamisura['metabolismo'] = round(
            #         primamisura['metabolismo'], 2)
            #     registraprimamisura.save()
            #     can.drawRightString(415, 519, (str(
            #         round(primamisura['metabolismo']-registraprimamisura['metabolismo'], 2))))

            if penultimamisura['metabolismo']:
                can.drawRightString(
                    315, 519, (str(round(penultimamisura['metabolismo'], 2))))
                can.drawRightString(
                    365, 519, (str(round(primamisura['metabolismo']-penultimamisura['metabolismo'], 2))))
            else:
                can.drawRightString(308, 521, ('--'))
                can.drawRightString(358, 521, ('--'))
    else:
        can.drawRightString(258, 521, ('--'))
        can.drawRightString(308, 521, ('--'))
        can.drawRightString(358, 521, ('--'))
        can.drawRightString(408, 521, ('--'))
    # riga9
    if primamisura['grasso_viscerale']:
        can.drawRightString(
            265, 500, (str(round(primamisura['grasso_viscerale'], 2))))
        if primamisurazione:
            can.drawRightString(308, 500, ('--'))
            can.drawRightString(358, 500, ('--'))
            can.drawRightString(408, 500, ('--'))
        else:
            if ultimamisura['grasso_viscerale']:
                can.drawRightString(415, 502, (str(
                    round(primamisura['grasso_viscerale']-ultimamisura['grasso_viscerale'], 2))))
            # else:
            #     registraprimamisura = get_object_or_404(
            #         PersonalCheckUpCliente, pk=ultimamisura.pk)
            #     registraprimamisura['grasso_viscerale'] = round(
            #         primamisura['grasso_viscerale'], 2)
            #     registraprimamisura.save()
            #     can.drawRightString(415, 502, (str(
            #         round(primamisura['grasso_viscerale']-registraprimamisura['grasso_viscerale'], 2))))

            if penultimamisura['grasso_viscerale']:
                can.drawRightString(
                    315, 502, (str(round(penultimamisura['grasso_viscerale'], 2))))
                can.drawRightString(365, 502, (str(
                    round(primamisura['grasso_viscerale']-penultimamisura['grasso_viscerale'], 2))))
            else:
                can.drawRightString(308, 500, ('--'))
                can.drawRightString(358, 500, ('--'))
    else:
        can.drawRightString(258, 502, ('--'))
        can.drawRightString(308, 502, ('--'))
        can.drawRightString(358, 502, ('--'))
        can.drawRightString(408, 502, ('--'))

    # riga10
    can.drawRightString(265, 483, (str(round(primamisura['collocm'], 2))))
    if primamisurazione:
        can.drawRightString(308, 483, ('--'))
        can.drawRightString(358, 483, ('--'))
        can.drawRightString(408, 483, ('--'))
    else:
        can.drawRightString(
            315, 483, (str(round(penultimamisura['collocm'], 2))))
        can.drawRightString(
            365, 483, (str(round(primamisura['collocm']-penultimamisura['collocm'], 2))))
        can.drawRightString(
            415, 483, (str(round(primamisura['collocm']-ultimamisura['collocm'], 2))))

    # riga11
    can.drawRightString(265, 464, (str(round(primamisura['toracecm'], 2))))
    if primamisurazione:
        can.drawRightString(308, 464, ('--'))
        can.drawRightString(358, 464, ('--'))
        can.drawRightString(408, 464, ('--'))
    else:
        can.drawRightString(
            315, 464, (str(round(penultimamisura['toracecm'], 2))))
        can.drawRightString(
            365, 464, (str(round(primamisura['toracecm']-penultimamisura['toracecm'], 2))))
        can.drawRightString(
            415, 464, (str(round(primamisura['toracecm']-ultimamisura['toracecm'], 2))))

    # riga12
    can.drawRightString(265, 445, (str(round(primamisura['cosciadxcm'], 2))))
    if primamisurazione:
        can.drawRightString(308, 445, ('--'))
        can.drawRightString(358, 445, ('--'))
        can.drawRightString(408, 445, ('--'))
    else:
        can.drawRightString(
            315, 445, (str(round(penultimamisura['cosciadxcm'], 2))))
        can.drawRightString(
            365, 445, (str(round(primamisura['cosciadxcm']-penultimamisura['cosciadxcm'], 2))))
        can.drawRightString(
            415, 445, (str(round(primamisura['cosciadxcm']-ultimamisura['cosciadxcm'], 2))))

    # riga13
    can.drawRightString(265, 426, (str(round(primamisura['cosciasxcm'], 2))))
    if primamisurazione:
        can.drawRightString(308, 426, ('--'))
        can.drawRightString(358, 426, ('--'))
        can.drawRightString(408, 426, ('--'))
    else:
        can.drawRightString(
            315, 426, (str(round(penultimamisura['cosciasxcm'], 2))))
        can.drawRightString(
            365, 426, (str(round(primamisura['cosciasxcm']-penultimamisura['cosciasxcm'], 2))))
        can.drawRightString(
            415, 426, (str(round(primamisura['cosciasxcm']-ultimamisura['cosciasxcm'], 2))))

    # riga14
    can.drawRightString(265, 407, (str(round(primamisura['fianchicm'], 2))))
    if primamisurazione:
        can.drawRightString(308, 407, ('--'))
        can.drawRightString(358, 407, ('--'))
        can.drawRightString(408, 407, ('--'))
    else:
        can.drawRightString(
            315, 407, (str(round(penultimamisura['fianchicm'], 2))))
        can.drawRightString(
            365, 407, (str(round(primamisura['fianchicm']-penultimamisura['fianchicm'], 2))))
        can.drawRightString(
            415, 407, (str(round(primamisura['fianchicm']-ultimamisura['fianchicm'], 2))))

    # riga15
    can.drawRightString(265, 388, (str(round(primamisura['addomecm'], 2))))
    if primamisurazione:
        can.drawRightString(308, 388, ('--'))
        can.drawRightString(358, 388, ('--'))
        can.drawRightString(408, 388, ('--'))
    else:
        can.drawRightString(
            315, 388, (str(round(penultimamisura['addomecm'], 2))))
        can.drawRightString(
            365, 388, (str(round(primamisura['addomecm']-penultimamisura['addomecm'], 2))))
        can.drawRightString(
            415, 388, (str(round(primamisura['addomecm']-ultimamisura['addomecm'], 2))))

    # riga16
    can.drawRightString(
        265, 369, (str(round(primamisura['ginocchiodxcm'], 2))))
    if primamisurazione:
        can.drawRightString(308, 369, ('--'))
        can.drawRightString(358, 369, ('--'))
        can.drawRightString(408, 369, ('--'))
    else:
        can.drawRightString(
            315, 369, (str(round(penultimamisura['ginocchiodxcm'], 2))))
        can.drawRightString(365, 369, (str(
            round(primamisura['ginocchiodxcm']-penultimamisura['ginocchiodxcm'], 2))))
        can.drawRightString(
            415, 369, (str(round(primamisura['ginocchiodxcm']-ultimamisura['ginocchiodxcm'], 2))))

    # riga17
    can.drawRightString(
        265, 350, (str(round(primamisura['ginocchiosxcm'], 2))))
    if primamisurazione:
        can.drawRightString(308, 350, ('--'))
        can.drawRightString(358, 350, ('--'))
        can.drawRightString(408, 350, ('--'))
    else:
        can.drawRightString(
            315, 350, (str(round(penultimamisura['ginocchiosxcm'], 2))))
        can.drawRightString(365, 350, (str(
            round(primamisura['ginocchiosxcm']-penultimamisura['ginocchiosxcm'], 2))))
        can.drawRightString(
            415, 350, (str(round(primamisura['ginocchiosxcm']-ultimamisura['ginocchiosxcm'], 2))))

    if cliente['sesso'] == 'F':
        # ovale tabella femminile
        p = can.beginPath()
        bmi_ottimale = 23.8
        if primamisura['bmi'] < 18.5:
            p.roundRect(99, 191, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        elif primamisura['bmi'] >= 18.5 and primamisura['bmi'] < 23.9:
            p.roundRect(99, 175, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        elif primamisura['bmi'] >= 23.9 and primamisura['bmi'] < 28.7:
            p.roundRect(99, 159, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        elif primamisura['bmi'] >= 28.7 and primamisura['bmi'] < 35:
            p.roundRect(99, 142, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        elif primamisura['bmi'] >= 35 and primamisura['bmi'] < 40:
            p.roundRect(99, 125, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        else:
            p.roundRect(99, 109, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
    else:
        # ovale tabella maschile
        p = can.beginPath()
        bmi_ottimale = 24.9
        if primamisura['bmi'] < 18.5:
            p.roundRect(357, 191, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        elif primamisura['bmi'] >= 18.5 and primamisura['bmi'] < 23.9:
            p.roundRect(357, 175, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        elif primamisura['bmi'] >= 23.9 and primamisura['bmi'] < 28.7:
            p.roundRect(357, 159, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        elif primamisura['bmi'] >= 28.7 and primamisura['bmi'] < 35:
            p.roundRect(357, 142, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        elif primamisura['bmi'] >= 35 and primamisura['bmi'] < 40:
            p.roundRect(357, 125, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)
        else:
            p.roundRect(357, 109, 157, 15, 5)
            can.setStrokeColorRGB(255, 0, 0)
            can.drawPath(p, stroke=1, fill=0)

    # riga17
    # calcolo stato attuale e del bmi
    bmi = primamisura['bmi']
    sesso = cliente['sesso']

    url_backend = settings.BASE_URL + 'utils/statobmi/' + \
        str(id) + '/' + str(bmi)

    headers = {"Authorization": f"Token {request.session['auth_token']}"}
    response = requests.get(url_backend, headers=headers)
    if response.status_code == 200:
        stato_peso = response.json()

    can.drawRightString(190, 63, (str(stato_peso)))
    can.drawRightString(345, 63, (str(primamisura['peso_ottimale'])))
    can.drawRightString(480, 63, (str(cliente['peso_desiderato'])))

    # riga18
    # can.drawString(320, 42, (str(primamisura.programma.nome_programma)))

    can.showPage()
    can.save()

    packet1 = io.BytesIO()
    # create a new PDF with Reportlab
    can1 = canvas.Canvas(packet1, pagesize=letter)
    #
    # can.setFillColorRGB(1,0,0) #choose your font colour
    can1.setFont("Helvetica", 10)

    # tabella muscolatura scheletrica
    if primamisura['muscolatura']:
        if cliente['sesso'] == 'F':
            p = can1.beginPath()
            if eta < 40:
                if primamisura['muscolatura'] < 24.4:
                    p.roundRect(343, 700, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 24.4 and primamisura['muscolatura'] < 30.4:
                    p.roundRect(384, 700, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 30.4 and primamisura['muscolatura'] < 35.4:
                    p.roundRect(430, 700, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 35.4:
                    p.roundRect(484, 700, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
            elif eta >= 40 and eta < 60:
                if primamisura['muscolatura'] < 24.4:
                    p.roundRect(343, 690, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 24.4 and primamisura['muscolatura'] < 30.4:
                    p.roundRect(384, 690, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 30.4 and primamisura['muscolatura'] < 35.4:
                    p.roundRect(430, 690, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 35.4:
                    p.roundRect(484, 690, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
            elif eta >= 60:
                if primamisura['muscolatura'] < 24.4:
                    p.roundRect(343, 680, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 24.4 and primamisura['muscolatura'] < 30.4:
                    p.roundRect(384, 680, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 30.4 and primamisura['muscolatura'] < 35.4:
                    p.roundRect(430, 680, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 35.4:
                    p.roundRect(484, 680, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
        else:
            p = can1.beginPath()
            if eta < 40:
                if primamisura['muscolatura'] < 24.4:
                    p.roundRect(343, 670, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 24.4 and primamisura['muscolatura'] < 30.4:
                    p.roundRect(384, 670, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 30.4 and primamisura['muscolatura'] < 35.4:
                    p.roundRect(430, 670, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 35.4:
                    p.roundRect(484, 670, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
            elif eta >= 40 and eta < 60:
                if primamisura['muscolatura'] < 24.4:
                    p.roundRect(343, 659, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 24.4 and primamisura['muscolatura'] < 30.4:
                    p.roundRect(384, 659, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 30.4 and primamisura['muscolatura'] < 35.4:
                    p.roundRect(430, 659, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 35.4:
                    p.roundRect(484, 659, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
            elif eta >= 60:
                if primamisura['muscolatura'] < 24.4:
                    p.roundRect(343, 649, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 24.4 and primamisura['muscolatura'] < 30.4:
                    p.roundRect(384, 649, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 30.4 and primamisura['muscolatura'] < 35.4:
                    p.roundRect(430, 649, 37, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)
                elif primamisura['muscolatura'] >= 35.4:
                    p.roundRect(484, 649, 29, 10, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(p, stroke=1, fill=0)

    # tabella massa grassa
    if primamisura['grasso_corporeo']:
        if cliente['sesso'] == 'F':
            g = can1.beginPath()
            if eta > 17 and eta <= 29:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 20:
                    g.roundRect(308, 510, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 20 and primamisura['grasso_corporeo'] < 28:
                    g.roundRect(361, 510, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 28 and primamisura['grasso_corporeo'] < 36:
                    g.roundRect(414, 510, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 36 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(467, 510, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
            elif eta >= 30 and eta <= 39:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 22:
                    g.roundRect(308, 498, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 22 and primamisura['grasso_corporeo'] < 30:
                    g.roundRect(361, 498, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 30 and primamisura['grasso_corporeo'] < 38:
                    g.roundRect(404, 498, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 38 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(466, 498, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
            elif eta >= 40 and eta <= 49:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 24:
                    g.roundRect(308, 485, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 24 and primamisura['grasso_corporeo'] < 32:
                    g.roundRect(361, 485, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 32 and primamisura['grasso_corporeo'] < 40:
                    g.roundRect(404, 485, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 40 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(466, 485, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
            elif eta >= 50 and eta <= 59:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 26:
                    g.roundRect(308, 472, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 26 and primamisura['grasso_corporeo'] < 34:
                    g.roundRect(361, 472, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 34 and primamisura['grasso_corporeo'] < 42:
                    g.roundRect(404, 472, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 42 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(466, 472, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
            else:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 28:
                    g.roundRect(308, 459, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 28 and primamisura['grasso_corporeo'] < 36:
                    g.roundRect(361, 459, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 36 and primamisura['grasso_corporeo'] < 44:
                    g.roundRect(404, 459, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 44 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(466, 459, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
        else:
            g = can1.beginPath()
            if eta > 17 and eta <= 29:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 8:
                    g.roundRect(334, 510, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 8 and primamisura['grasso_corporeo'] < 18:
                    g.roundRect(387, 510, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 18 and primamisura['grasso_corporeo'] < 24:
                    g.roundRect(440, 510, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 24 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(493, 510, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
            elif eta >= 30 and eta <= 39:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 11:
                    g.roundRect(334, 498, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 11 and primamisura['grasso_corporeo'] < 20:
                    g.roundRect(387, 498, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 20 and primamisura['grasso_corporeo'] < 26:
                    g.roundRect(440, 498, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 26 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(493, 498, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
            elif eta >= 40 and eta <= 49:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 13:
                    g.roundRect(334, 485, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 13 and primamisura['grasso_corporeo'] < 22:
                    g.roundRect(387, 485, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 22 and primamisura['grasso_corporeo'] < 26:
                    g.roundRect(440, 485, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 26 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(493, 485, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
            elif eta >= 50 and eta <= 59:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 15:
                    g.roundRect(334, 472, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 15 and primamisura['grasso_corporeo'] < 24:
                    g.roundRect(387, 472, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 24 and primamisura['grasso_corporeo'] < 30:
                    g.roundRect(440, 472, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 3 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(493, 472, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
            else:
                if primamisura['grasso_corporeo'] >= 0 and primamisura['grasso_corporeo'] < 17:
                    g.roundRect(334, 459, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 17 and primamisura['grasso_corporeo'] < 26:
                    g.roundRect(387, 459, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 26 and primamisura['grasso_corporeo'] < 34:
                    g.roundRect(440, 459, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)
                elif primamisura['grasso_corporeo'] >= 34 and primamisura['grasso_corporeo'] < 99:
                    g.roundRect(493, 459, 24, 9, 2)
                    can1.setStrokeColorRGB(255, 0, 0)
                    can1.drawPath(g, stroke=1, fill=0)

    if primamisura['grasso_viscerale']:
        can1.drawString(140, 256, str(
            round(primamisura['grasso_viscerale'], 2)))
        v = can1.beginPath()
        if primamisura['grasso_viscerale'] >= 1 and primamisura['grasso_viscerale'] < 10:
            v.roundRect(130, 218, 300, 11, 2)
            can1.setStrokeColorRGB(255, 0, 0)
            can1.drawPath(v, stroke=1, fill=0)
        elif primamisura['grasso_viscerale'] >= 10 and primamisura['grasso_viscerale'] < 15:
            v.roundRect(130, 204, 300, 11, 2)
            can1.setStrokeColorRGB(255, 0, 0)
            can1.drawPath(v, stroke=1, fill=0)
        else:
            v.roundRect(130, 190, 300, 11, 2)
            can1.setStrokeColorRGB(255, 0, 0)
            can1.drawPath(v, stroke=1, fill=0)

    # firma

    can1.drawString(210, 30, str(datetime.now().strftime("%m/%d/%Y")))
    can1.drawString(310, 30, str(
        "firmato da " + cliente['cognome'] + " " + cliente['nome']))
    can1.drawString(310, 22, str("con email inviata a  " + cliente['email']))

    can1.showPage()
    can1.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    # read your existing PDF

    existing_pdf = PdfReader(open("static/static_file/personal.pdf", "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    output.add_page(page)

    page = existing_pdf.pages[1]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    packet1.seek(0)
    new_pdf = PdfReader(packet1)
    page = existing_pdf.pages[2]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    page = existing_pdf.pages[3]
    output.add_page(page)

    cartella_destinazione = 'pdf/' + str(cliente['codice_fiscale'])

    # Verifica e crea la cartella se non esiste
    if not os.path.exists(cartella_destinazione):
        try:
            os.makedirs(cartella_destinazione)
            print(f"Cartella '{cartella_destinazione}' creata con successo.")
        except OSError as e:
            print(
                f"Errore durante la creazione della cartella '{cartella_destinazione}': {e}")
    else:
        print(f"La cartella '{cartella_destinazione}' esiste già.")

    # Ora puoi aprire il file PDF nella cartella specificata
    nome_file_pdf = f"{data_corrente}-personal.pdf"
    percorso_completo_pdf = os.path.join(cartella_destinazione, nome_file_pdf)

    outputStream = open(percorso_completo_pdf, "wb")
    output.write(outputStream)
    outputStream.close()

    return percorso_completo_pdf
