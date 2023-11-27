import pdb
from django import forms
from django.shortcuts import redirect
from django.conf import settings
import requests


class FormCliente(forms.Form):

    nome = forms.CharField(max_length=100, label='Nome:',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control font-custom', 'placeholder': 'Nome'}),
                           error_messages={'required': 'Il nome è obbligatorio.'})
    cognome = forms.CharField(max_length=100, label='Cognome:',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control font-custom', 'placeholder': 'Cognome'}),
                              error_messages={'required': 'Il cognome è obbligatorio.'})
    citta_nascita = forms.CharField(max_length=100, label='Città di nascita:',
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control font-custom', 'placeholder': 'citta_nascita'}),
                                    error_messages={'required': 'La città di nascita è obbligatoria.'})
    provincia_nascita = forms.CharField(max_length=50, label='Provincia di Nascita',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control font-custom', 'placeholder': 'Provincia di nascita'}),
                                        error_messages={'required': 'Il campo Provincia di nascita è obbligatorio.'})
    stato_nascita = forms.CharField(max_length=50, label='Stato di Nascita',
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control font-custom', 'placeholder': 'Stato di nascita:'}),
                                    error_messages={'required': 'Il campo Stato di nascita è obbligatorio.'})
    data_nascita = forms.DateField(label='Data di nascita:',
                                   widget=forms.DateInput(
                                       attrs={'class': 'form-control font-custom', 'type': 'date'}),
                                   error_messages={'required': 'La data di nascita è obbligatoria.'})
    indirizzo = forms.CharField(max_length=100, label='Indirizzo di residenza:',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'indirizzo'}),
                                error_messages={'required': "L'indirizzo è obbligatorio."})
    cap = forms.CharField(max_length=10, label='Cap:',
                          widget=forms.NumberInput(
                              attrs={'class': 'form-control font-custom', 'placeholder': 'cap'}),
                          error_messages={'required': 'Il cap è obbligatorio.'})
    citta = forms.CharField(max_length=100, label='Citta di Residenza:',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control font-custom', 'placeholder': 'citta'}),
                            error_messages={'required': 'La città è obbligatorio.'})
    provincia = forms.CharField(max_length=50, label='Provincia di Residenza',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'Provincia di Residenza:'}),
                                error_messages={'required': 'Il campo Provincia di Residenza è obbligatorio.'})
    stato = forms.CharField(max_length=50, label='Stato di Residenza',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control font-custom', 'placeholder': 'Stato di Residenza:'}),
                            error_messages={'required': 'Il campo Stato di Residenza è obbligatorio.'})
    codice_fiscale = forms.CharField(max_length=16, label='Codice fiscale:',
                                     widget=forms.TextInput(
                                         attrs={'class': 'form-control font-custom', 'placeholder': 'codice_fiscale'}),
                                     error_messages={'required': 'La città è obbligatorio.'})
    telefono = forms.CharField(max_length=20, label='Telefono:', required=False,
                               widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'telefono'}))
    cellulare = forms.CharField(max_length=20, label='Cellulare:',
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'cellulare'}),
                                error_messages={'required': 'Il cellulare è obbligatorio.'})
    email = forms.EmailField(label='Email:',
                             widget=forms.EmailInput(
                                 attrs={'class': "form-control font-custom", 'placeholder': 'email'}),
                             error_messages={'required': "L'email è obbligatoria.", 'invalid': 'L\'indirizzo email non è valido.'})
    sesso = forms.CharField(label='Sesso:',
                            widget=forms.Select(choices=[('M', 'M'), ('F', 'F')], attrs={
                                                'class': 'form-select font-custom'}),
                            error_messages={'required': 'Il sesso è obbligatorio.'})
    note = forms.CharField(label='Note:', required=False,
                           widget=forms.Textarea(attrs={'class': "form-control font-custom", 'placeholder': 'note'}))


class FormClientePiva(forms.Form):

    nome = forms.CharField(max_length=100, label='Nome:',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control font-custom', 'placeholder': 'Nome'}),
                           error_messages={'required': 'Il nome è obbligatorio.'})
    cognome = forms.CharField(max_length=100, label='Cognome:',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control font-custom', 'placeholder': 'Cognome'}),
                              error_messages={'required': 'Il cognome è obbligatorio.'})
    citta_nascita = forms.CharField(max_length=100, label='Città di nascita:',
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control font-custom', 'placeholder': 'citta_nascita'}),
                                    error_messages={'required': 'La città di nascita è obbligatoria.'})
    provincia_nascita = forms.CharField(max_length=50, label='Provincia di Nascita',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control font-custom', 'placeholder': 'Provincia di nascita'}),
                                        error_messages={'required': 'Il campo Provincia di nascita è obbligatorio.'})
    stato_nascita = forms.CharField(max_length=50, label='Stato di Nascita',
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control font-custom', 'placeholder': 'Stato di nascita:'}),
                                    error_messages={'required': 'Il campo Stato di nascita è obbligatorio.'})
    data_nascita = forms.DateField(label='Data di nascita:',
                                   widget=forms.DateInput(
                                       attrs={'class': 'form-control font-custom', 'type': 'date'}),
                                   error_messages={'required': 'La data di nascita è obbligatoria.'})
    indirizzo = forms.CharField(max_length=100, label='Indirizzo di residenza:',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'indirizzo'}),
                                error_messages={'required': "L'indirizzo è obbligatorio."})
    cap = forms.CharField(max_length=10, label='Cap:',
                          widget=forms.NumberInput(
                              attrs={'class': 'form-control font-custom', 'placeholder': 'cap'}),
                          error_messages={'required': 'Il cap è obbligatorio.'})
    citta = forms.CharField(max_length=100, label='Citta di Residenza:',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control font-custom', 'placeholder': 'citta'}),
                            error_messages={'required': 'La città è obbligatorio.'})
    provincia = forms.CharField(max_length=50, label='Provincia di Residenza',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'Provincia di Residenza:'}),
                                error_messages={'required': 'Il campo Provincia di Residenza è obbligatorio.'})
    stato = forms.CharField(max_length=50, label='Stato di Residenza',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control font-custom', 'placeholder': 'Stato di Residenza:'}),
                            error_messages={'required': 'Il campo Stato di Residenza è obbligatorio.'})
    codice_fiscale = forms.CharField(max_length=16, label='Codice fiscale:',
                                     widget=forms.TextInput(
                                         attrs={'class': 'form-control font-custom', 'placeholder': 'codice_fiscale'}),
                                     error_messages={'required': 'La città è obbligatorio.'})
    telefono = forms.CharField(max_length=20, label='Telefono:', required=False,
                               widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'telefono'}))
    cellulare = forms.CharField(max_length=20, label='Cellulare:',
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'cellulare'}),
                                error_messages={'required': 'Il cellulare è obbligatorio.'})
    email = forms.EmailField(label='Email:',
                             widget=forms.EmailInput(
                                 attrs={'class': "form-control font-custom", 'placeholder': 'email'}),
                             error_messages={'required': "L'email è obbligatoria.", 'invalid': 'L\'indirizzo email non è valido.'})
    sesso = forms.CharField(label='Sesso:',
                            widget=forms.Select(choices=[('M', 'M'), ('F', 'F')], attrs={
                                                'class': 'form-select font-custom'}),
                            error_messages={'required': 'Il sesso è obbligatorio.'})
    note = forms.CharField(label='Note:', required=False,
                           widget=forms.Textarea(attrs={'class': "form-control font-custom", 'placeholder': 'note'}))
    ragione_sociale = forms.CharField(max_length=100, label='Ragione sociale:',
                                      widget=forms.TextInput(attrs={'class': 'form-control font-custom', 'placeholder': 'ragione_sociale'}))
    sede = forms.CharField(max_length=100, label='Sede:',
                           widget=forms.TextInput(attrs={'class': 'form-control font-custom', 'placeholder': 'sede'}))
    indirizzo_sede = forms.CharField(max_length=100, label='Indirizzo sede:',
                                     widget=forms.TextInput(attrs={'class': 'form-control font-custom', 'placeholder': 'indirizzo_sede'}))
    cap_sede = forms.CharField(max_length=10, label='Cap sede:',
                               widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'cap_sede'}))
    telefono_sede = forms.CharField(max_length=10, label='Telefono sede:', required=False,
                                    widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'telefono_sede'}))
    email_sede = forms.EmailField(label='Email sede:', required=False,
                                  widget=forms.EmailInput(
                                      attrs={'class': "form-control font-custom", 'placeholder': 'email_sede'}),
                                  error_messages={'invalid': 'L\'indirizzo email non è valido.'})
    partita_iva = forms.CharField(max_length=10, label='Partita iva:',
                                  widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'partita_iva'}))
    codice_univoco = forms.CharField(max_length=100, label='Codice univoco:',
                                     widget=forms.TextInput(attrs={'class': 'form-control font-custom', 'placeholder': 'codice_univoco'}))

    def clean(self):

        cleaned_data = super(FormClientePiva, self).clean()

        ragione_sociale = cleaned_data.get('ragione_sociale')
        sede = cleaned_data.get('sede')
        indirizzo_sede = cleaned_data.get('indirizzo_sede')
        cap_sede = cleaned_data.get('cap_sede')
        partita_iva = cleaned_data.get('partita_iva')
        codice_univoco = cleaned_data.get('codice_univoco')

        if ragione_sociale is None:
            self.errors['ragione_sociale'] = [
                'La ragione sociale è obbligatorio']

        if sede is None:
            self.errors['sede'] = ['La città della sede è obbligatorio']

        if indirizzo_sede is None:
            self.errors['indirizzo_sede'] = [
                'L\'indirizzo della sede sociale è obbligatorio']

        if partita_iva is None:
            self.errors['partita_iva'] = ['La partita iva è obbligatorio']

        if cap_sede is None:
            self.errors['cap_sede'] = [
                'Il cap della sede sociale è obbligatorio']

        if codice_univoco is None:
            self.errors['codice_univoco'] = [
                'Il codice univoco è obbligatorio']

        return cleaned_data


class FormClienteMinore(forms.Form):

    nome = forms.CharField(max_length=100, label='Nome:',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control font-custom', 'placeholder': 'Nome'}),
                           error_messages={'required': 'Il nome è obbligatorio.'})
    cognome = forms.CharField(max_length=100, label='Cognome:',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control font-custom', 'placeholder': 'Cognome'}),
                              error_messages={'required': 'Il cognome è obbligatorio.'})
    citta_nascita = forms.CharField(max_length=100, label='Città di nascita:',
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control font-custom', 'placeholder': 'citta_nascita'}),
                                    error_messages={'required': 'La città di nascita è obbligatoria.'})
    provincia_nascita = forms.CharField(max_length=50, label='Provincia di Nascita',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control font-custom', 'placeholder': 'Provincia di nascita'}),
                                        error_messages={'required': 'Il campo Provincia di nascita è obbligatorio.'})
    stato_nascita = forms.CharField(max_length=50, label='Stato di Nascita',
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control font-custom', 'placeholder': 'Stato di nascita:'}),
                                    error_messages={'required': 'Il campo Stato di nascita è obbligatorio.'})
    data_nascita = forms.DateField(label='Data di nascita:',
                                   widget=forms.DateInput(
                                       attrs={'class': 'form-control font-custom', 'type': 'date'}),
                                   error_messages={'required': 'La data di nascita è obbligatoria.'})
    indirizzo = forms.CharField(max_length=100, label='Indirizzo di residenza:',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'indirizzo'}),
                                error_messages={'required': "L'indirizzo è obbligatorio."})
    cap = forms.CharField(max_length=10, label='Cap:',
                          widget=forms.NumberInput(
                              attrs={'class': 'form-control font-custom', 'placeholder': 'cap'}),
                          error_messages={'required': 'Il cap è obbligatorio.'})
    citta = forms.CharField(max_length=100, label='Citta:',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control font-custom', 'placeholder': 'citta'}),
                            error_messages={'required': 'La città è obbligatorio.'})
    provincia = forms.CharField(max_length=50, label='Provincia di Residenza',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'Provincia di Residenza:'}),
                                error_messages={'required': 'Il campo Provincia di Residenza è obbligatorio.'})
    stato = forms.CharField(max_length=50, label='Stato di Residenza',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control font-custom', 'placeholder': 'Stato di Residenza:'}),
                            error_messages={'required': 'Il campo Stato di Residenza è obbligatorio.'})
    codice_fiscale = forms.CharField(max_length=16, label='Codice fiscale:',
                                     widget=forms.TextInput(
                                         attrs={'class': 'form-control font-custom', 'placeholder': 'codice_fiscale'}),
                                     error_messages={'required': 'La città è obbligatorio.'})
    telefono = forms.CharField(max_length=20, label='Telefono:', required=False,
                               widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'telefono'}))
    cellulare = forms.CharField(max_length=20, label='Cellulare:',
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'cellulare'}),
                                error_messages={'required': 'Il cellulare è obbligatorio.'})
    email = forms.EmailField(label='Email:',
                             widget=forms.EmailInput(
                                 attrs={'class': "form-control font-custom", 'placeholder': 'email'}),
                             error_messages={'required': "L'email è obbligatoria.", 'invalid': 'L\'indirizzo email non è valido.'})
    sesso = forms.CharField(label='Sesso:',
                            widget=forms.Select(choices=[('M', 'M'), ('F', 'F')], attrs={
                                                'class': 'form-select font-custom'}),
                            error_messages={'required': 'Il sesso è obbligatorio.'})
    note = forms.CharField(label='Note:', required=False,
                           widget=forms.Textarea(attrs={'class': "form-control font-custom", 'placeholder': 'note'}))
    beneficiario_nome = forms.CharField(max_length=100, label='Beneficiario nome:',
                                        widget=forms.TextInput(attrs={'class': 'form-control font-custom', 'placeholder': 'beneficiario_nome'}))
    beneficiario_cognome = forms.CharField(max_length=100, label='Beneficiario cognome:',
                                           widget=forms.TextInput(attrs={'class': 'form-control font-custom', 'placeholder': 'beneficiario_cognome'}))
    beneficiario_codice_fiscale = forms.CharField(max_length=100, label='Beneficiario codice fiscale:',
                                                  widget=forms.TextInput(attrs={'class': 'form-control font-custom', 'placeholder': 'beneficiario_codice_fiscale'}))
    beneficiario_cellulare = forms.CharField(max_length=10, label='Beneficiario cellulare:', required=False,
                                             widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'beneficiario_cellulare'}))

    def clean(self):

        cleaned_data = super(FormClienteMinore, self).clean()

        beneficiario_nome = cleaned_data.get('beneficiario_nome')
        beneficiario_cognome = cleaned_data.get('beneficiario_cognome')
        beneficiario_codice_fiscale = cleaned_data.get(
            'beneficiario_codice_fiscale')

        if beneficiario_nome is None:
            self.errors['beneficiario_nome'] = [
                'Il nome del beneficiario è obbligatorio']

        if beneficiario_cognome is None:
            self.errors['beneficiario_cognome'] = [
                'Il cognome del beneficiario è obbligatorio']

        if beneficiario_codice_fiscale is None:
            self.errors['beneficiario_codice_fiscale'] = [
                'Il codice fiscale del beneficiario è obbligatorio']

        return cleaned_data


class ClientiSearchForm(forms.Form):

    search_query = forms.CharField(
        label='Cerca:',
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Cerca'}),
    )


class FormMisure(forms.Form):

    peso = forms.FloatField(label='Peso:',
                            widget=forms.NumberInput(
                                attrs={'class': 'form-control font-custom', 'placeholder': 'peso'}),
                            error_messages={'required': 'Il peso è obbligatorio.'})
    altezza = forms.FloatField(label='Altezza in cm:',
                               widget=forms.NumberInput(
                                   attrs={'class': 'form-control font-custom', 'placeholder': 'altezza'}),
                               error_messages={'required': 'L\'altezza è obbligatoria.'})
    eta = forms.FloatField(label='Età:',
                           widget=forms.NumberInput(
                               attrs={'class': 'form-control font-custom', 'placeholder': 'eta', 'readonly': True}),
                           error_messages={'required': 'L\'eta è obbligatoria.'})
    bmi = forms.FloatField(label='Bmi:',
                           widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'bmi', 'readonly': True}))
    grasso_corporeo = forms.FloatField(label='Percentuale grasso corporeo:', required=False,
                                       widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'grasso_corporeo'}))
    muscolatura = forms.FloatField(label='Muscolatura:', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'muscolatura'}))
    metabolismo = forms.FloatField(label='Metabolismo:', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'metabolismo'}))
    grasso_viscerale = forms.FloatField(label='Percentuale grasso viscerale:', required=False,
                                        widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'grasso_viscerale'}))
    collocm = forms.FloatField(label='Misura cm collo:',
                               widget=forms.NumberInput(
                                   attrs={'class': 'form-control font-custom', 'placeholder': 'collocm'}),
                               error_messages={'required': 'la misura è obbligatoria.'})
    toracecm = forms.FloatField(label='Misura cm torace:',
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'toracecm'}),
                                error_messages={'required': 'la misura è obbligatoria.'})
    cosciadxcm = forms.FloatField(label='Misura cm coscia destra:',
                                  widget=forms.NumberInput(
                                      attrs={'class': 'form-control font-custom', 'placeholder': 'cosciadxcm'}),
                                  error_messages={'required': 'la misura è obbligatoria.'})
    cosciasxcm = forms.FloatField(label='Misura cm coscia sinistra:',
                                  widget=forms.NumberInput(
                                      attrs={'class': 'form-control font-custom', 'placeholder': 'cosciasxcm'}),
                                  error_messages={'required': 'la misura è obbligatoria.'})
    fianchicm = forms.FloatField(label='Misura cm fianchi:',
                                 widget=forms.NumberInput(
                                     attrs={'class': 'form-control font-custom', 'placeholder': 'fianchicm'}),
                                 error_messages={'required': 'la misura è obbligatoria.'})
    addomecm = forms.FloatField(label='Misura cm addome:',
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'addomecm'}),
                                error_messages={'required': 'la misura è obbligatoria.'})
    ginocchiodxcm = forms.FloatField(label='Misura cm ginocchio destro:',
                                     widget=forms.NumberInput(
                                         attrs={'class': 'form-control font-custom', 'placeholder': 'ginocchiodxcm'}),
                                     error_messages={'required': 'la misura è obbligatoria.'})
    ginocchiosxcm = forms.FloatField(label='Misura cm ginocchio sinistro:',
                                     widget=forms.NumberInput(
                                         attrs={'class': 'form-control font-custom', 'placeholder': 'ginocchiosxcm'}),
                                     error_messages={'required': 'la misura è obbligatoria.'})
    cellulare = forms.CharField(max_length=20, label='Cellulare:',
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'cellulare'}),
                                error_messages={'required': 'Il cellulare è obbligatorio.'})
    email = forms.EmailField(label='Email:',
                             widget=forms.EmailInput(
                                 attrs={'class': "form-control font-custom", 'placeholder': 'email'}),
                             error_messages={'required': "L'email è obbligatoria.", 'invalid': 'L\'indirizzo email non è valido.'})


class FormMisureRiassunto(forms.Form):

    peso_ottimale = forms.FloatField(label='Peso ottimale:',
                                     widget=forms.NumberInput(
                                         attrs={'class': 'form-control font-custom', 'placeholder': 'peso_ottimale', 'readonly': True}))
    peso_desiderato = forms.IntegerField(label='Peso desiderato:',
                                         widget=forms.NumberInput(
                                             attrs={'class': 'form-control font-custom', 'placeholder': 'peso_desiderato'}))
    # programma_consigliato = UserModelChoiceField(queryset=Programmi.objects.filter(gruppo__nome_gruppo='MW- NUTRIGEN'))
    misura = forms.ChoiceField(label='Misura da Visualizzare:',
                               widget=forms.Select(
                                   attrs={'class': 'form-select font-custom', 'placeholder': 'misura'}),
                               required=False)

    def __init__(self, *args, **kwargs):

        lista_opzioni = kwargs.pop('lista_opzioni', [])

        super(FormMisureRiassunto, self).__init__(*args, **kwargs)

        self.fields['misura'].choices = lista_opzioni


class FormChiave(forms.Form):

    chiave = forms.CharField(label='Inserire codice:',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control font-custom', 'placeholder': 'chiave'}), error_messages={'required': 'Il cap è obbligatorio.'})


class ChoiceFieldNoValidation(forms.MultipleChoiceField):
    def validate(self, value):
        pass


SCELTA = (

    ('Si', 'Si'),
    ('No', 'No')
)

SCELTA3 = (

    ('Si', 'Si'),
    ('No', 'No'),
    ('A volte', 'A volte')
)

CIVILE = (
    ('Libero', 'Libero'),
    ('Coniugato', 'Coniugato')
)

FISICO = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E')
)

SCELTADIABETE = (

    ('Tipo 1', 'Tipo 1'),
    ('Tipo 2', 'Tipo 2')
)

MESIGRAVIDANZA = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9')

)

GIORNI = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7')
)

GRUPPO = (
    ('N', 'Non so'),
    ('0', '0'),
    ('A', 'A'),
    ('B', 'B'),
    ('AB', 'AB')
)

ALIMENTAZIONE = (
    ('Onnivoro', 'Onnivoro'),
    ('Vegetariano', 'Vegetariano'),
    ('Vegano', 'Vegano')
)
PRESSIONE = (
    ('Normale', 'Normale'),
    ('Ipoteso', 'Ipoteso'),
    ('Iperteso', 'Iperteso')
)
ALIMENTI = (
    ('Caffè', 'Caffè'),
    ('Pane', 'Pane'),
    ('Verdure', 'Verdure'),
    ('Carne', 'Carne'),
    ('Cereali', 'Cereali'),
    ('Cioccolata', 'Cioccolata'),
    ('Legumi', 'Legumi'),
    ('Alcolici', 'Alcolici'),
    ('Pasta', 'Pasta'),
    ('Frutta', 'Frutta'),
    ('Pesce', 'Pesce'),
    ('Dolci', 'Dolci'),
    ('Pizza', 'Pizza'),
    ('Latticini', 'Latticini')
)

SAPORI = (
    ('Piccante', 'Piccante'),
    ('Dolce', 'Dolce'),
    ('Salato', 'Salato'),
    ('Amaro', 'Amaro'),
    ('Aspro', 'Aspro'),
    ('Insipido', 'Insipido')
)

CAR1 = (

    ('Individualista', 'Individualista'),
    ('Altruista', 'Altruista')
)

CAR2 = (

    ('Estroverso', 'Estroverso'),
    ('Introverso', 'Introverso')
)

CAR3 = (

    ('Ottimista', 'Ottimista'),
    ('Pessimista', 'Pessimista')
)

SFOGO = (
    ('Dentro', 'Dentro'),
    ('Fuori', 'Fuori'),
    ('Non so', 'Non so')
)

GIORNATA = (
    ('Mattina', 'Mattina'),
    ('Pomeriggio', 'Pomeriggio'),
    ('Sera', 'Sera')
)

DETERMINATO = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10')
)

PASTI = (
    (1, 'Sempre'),
    (2, 'Colazione'),
    (3, 'Pranzo'),
    (4, 'Cena'),
    (5, 'Mai')

)


class ModuloInformazioniForm(forms.Form):

    professione = forms.CharField(
        max_length=50,
        label='Professione',
        widget=forms.TextInput(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Professione'}),
        error_messages={'required': 'Il campo Professione è obbligatorio.'}
    )

    stato_civile = forms.ChoiceField(
        choices=CIVILE,
        label='Stato Civile',
        widget=forms.RadioSelect(attrs={
                                 'class': 'form-control font-custom', 'placeholder': 'Stato civile:', 'id': 'rabbia_id'}),
        initial=None,
        error_messages={'required': 'Il campo Stato civile è obbligatorio.'}
    )

    maggiorenne = forms.ChoiceField(
        choices=SCELTA,
        label='Maggiorenne',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Maggiorenne?:'}),
        initial=None,
        error_messages={'required': 'Il campo Maggiorenne è obbligatorio.'}
    )

    peso_attuale = forms.CharField(
        max_length=5,
        label='Peso Attuale',
        widget=forms.NumberInput(
            attrs={'class': 'form-control font-custom',  'placeholder': 'Peso Attuale:'}),
        error_messages={'required': 'Il campo Peso attuale è obbligatorio.'}
    )

    altezza = forms.CharField(
        max_length=5,
        label='Altezza',
        widget=forms.NumberInput(attrs={
                                 'class': 'form-control font-custom',  'placeholder': 'Altezza in cm:', 'readonly': True}),
        error_messages={'required': 'Il campo Altezza è obbligatorio.'}
    )

    bmi = forms.FloatField(

        label='BMI',
        widget=forms.NumberInput(
            attrs={'class': 'form-control font-custom', 'placeholder': 'BMI:', 'readonly': True}),
        error_messages={'required': 'Il campo BMI è obbligatorio.'}
    )

    stato_attuale = forms.CharField(
        max_length=20,
        label='Stato Attuale',
        widget=forms.TextInput(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Stato Attuale:', 'readonly': True}),
        error_messages={'required': 'Il campo Stato attuale è obbligatorio.'}
    )

    peso_ottimale = forms.FloatField(

        label='Peso Ottimale',
        widget=forms.NumberInput(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Peso Ottimale:', 'readonly': True}),
        error_messages={'required': 'Il campo peso ottimale è obbligatorio.'}
    )

    scostamento_peso = forms.FloatField(

        label='Scostamento Peso',
        widget=forms.NumberInput(attrs={
                                 'class': 'form-control font-custom', 'placeholder': 'Scostamento Peso in KG:', 'readonly': True}),
        error_messages={
            'required': 'Il campo Scostamento peso in KG è obbligatorio.'}
    )

    peso_desiderato = forms.FloatField(

        label='Peso Desiderato',
        widget=forms.NumberInput(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Peso Desiderato:', 'readonly': True}),
        error_messages={'required': 'Il campo Peso desiderato è obbligatorio.'}
    )

    struttura_fisica = forms.ChoiceField(
        choices=FISICO,
        label='In quale struttura fisica ti riconosci?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'In quale struttura fisica ti riconosci?'}),
        initial=None,
        error_messages={
            'required': 'Il campo Struttura fisica è obbligatorio.'}

    )

    struttura_desiderata = forms.ChoiceField(
        choices=FISICO,
        label='Quale struttura ti piacerebbe avere?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'Quale struttura ti piacerebbe avere?'}),
        initial=None,
        error_messages={
            'required': 'Il campo Struttura desiderata è obbligatorio.'}
    )

    pressione_arteriosa = forms.ChoiceField(
        choices=PRESSIONE,
        label='Pressione Arteriosa:',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Pressione Arteriosa:'}),
        initial=None,
        error_messages={
            'required': 'Il campo Pressione arteriosa è obbligatorio.'}
    )

    diabete = forms.ChoiceField(
        choices=SCELTA,
        label='Soffri di diabete?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Soffri di diabete?'}),
        initial=None,
        error_messages={'required': 'Il campo Diabete è obbligatorio.'}
    )

    tipo_diabete = forms.ChoiceField(
        choices=SCELTADIABETE,
        required=False,
        label='Che tipo diabete:',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Che tipo diabete:'}),
        initial=None,
    )

    menopausa = forms.ChoiceField(
        choices=SCELTA,
        label='Sei in menopausa?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Sei in menopausa?'}),
        initial=None,
        required=False
    )

    gravidanza = forms.ChoiceField(
        choices=SCELTA,
        label='Hai una gravidanza in corso?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'Hai una gravidanza in corso?'}),
        initial=None,
        required=False
    )

    mesi_gravidanza = forms.ChoiceField(
        choices=MESIGRAVIDANZA,
        label='In che mese sei?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'In che mese sei?'}),
        initial=None,
        required=False
    )

    rapporto_corpo = forms.ChoiceField(
        choices=SCELTA3,
        label='Hai un buon rapporto con il tuo corpo?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'Hai un buon rapporto con il tuo corpo?'}),
        initial=None,
        error_messages={'required': 'Il campo Rapporto corpo è obbligatorio.'}
    )

    droghe = forms.ChoiceField(
        choices=SCELTA,
        label='Fai uso di droghe?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Fai uso di droghe?'}),
        initial=None,
        error_messages={'required': 'Il campo uso di droghe è obbligatorio.'}
    )

    allergie = forms.ChoiceField(
        choices=SCELTA,
        label='Soffri di allergie?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Soffri di allergie?'}),
        initial=None,
        error_messages={'required': 'Il campo allergie è obbligatorio.'}
    )

    allergie_elenco = forms.CharField(
        max_length=300,
        label='Quali?',
        widget=forms.Textarea(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Quali?'}),
        required=False
    )

    farmaci = forms.ChoiceField(
        choices=SCELTA,
        label='Assumi farmaci?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Assumi farmaci?'}),
        initial=None,
        error_messages={'required': 'Il campo farmaci è obbligatorio.'}
    )

    farmaci_elenco = forms.CharField(
        max_length=100,
        label='Quali?',
        widget=forms.Textarea(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Quali?'}),
        required=False
    )

    sport = forms.ChoiceField(
        choices=SCELTA,
        label='Sport',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Pratichi sport?'}),
        initial=None,
        error_messages={'required': 'Il campo sport è obbligatorio.'}
    )

    sport_praticato = forms.CharField(
        max_length=30,
        label='Quali?',
        widget=forms.Textarea(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Quali?'}),
        required=False
    )

    sport_praticato_giorni = forms.ChoiceField(
        choices=GIORNI,
        label='Giorni di Sport Praticato',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'Quante volte alla settimana?'}),
        required=False
    )

    gruppo_sanguigno = forms.ChoiceField(
        choices=GRUPPO,
        label='Quale è il tuo gruppo sanguigno?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'Quale è il tuo gruppo sanguigno?'}),
        initial=None,
        error_messages={
            'required': 'Il campo gruppo sanguigno è obbligatorio.'}
    )

    insonnia = forms.ChoiceField(
        choices=SCELTA3,
        label='Soffri di insonnia?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Soffri di insonnia?'}),
        initial=None,
        error_messages={'required': 'Il campo insonnia è obbligatorio.'}
    )

    stitichezza = forms.ChoiceField(
        choices=SCELTA3,
        label='Soffri di stitichezza?',
        widget=forms.RadioSelect(attrs={
            'class': 'form-control font-custom', 'placeholder': 'Soffri di stitichezza?'}),
        initial=None,
        error_messages={'required': 'Il campo stitichezza è obbligatorio.'}
    )

    fame_nervosa = forms.ChoiceField(
        choices=SCELTA3,
        label='Soffri di fame nervosa?',
        widget=forms.RadioSelect(attrs={
            'class': 'form-control font-custom', 'placeholder': 'Soffri di fame nervosa?'}),
        initial=None,
        error_messages={'required': 'Il campo fame nervosa è obbligatorio.'}
    )

    fumo = forms.ChoiceField(
        choices=SCELTA,
        label='Fumo',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Fumi?'}),
        initial=None,
        error_messages={'required': 'Il campo stitichezza è obbligatorio.'}
    )

    numero_sigarette = forms.CharField(
        max_length=3,
        label='Numero di Sigarette',
        widget=forms.TextInput(attrs={
                               'class': 'form-control font-custom', 'placeholder': 'Quante sigarette fumi al giorno??'}),
        required=False
    )

    delta_numero_sigarette = forms.CharField(
        max_length=3,
        label='Delta Numero di Sigarette',
        widget=forms.TextInput(attrs={
                               'class': 'form-control font-custom', 'placeholder': 'Differenza media nazionale?'}, ),
        required=False,
        disabled=True
    )

    gengive = forms.ChoiceField(
        choices=SCELTA3,
        label='Problemi di gengive?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Problemi di gengive?'}),
        initial=None,
        error_messages={'required': 'Il campo gengive è obbligatorio.'}
    )

    tatuaggi = forms.ChoiceField(
        choices=SCELTA,
        label='Hai tatuaggi?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai tatuaggi?'}),
        initial=None,
        error_messages={'required': 'Il campo tatuaggi è obbligatorio.'}
    )

    bevi_acqua = forms.ChoiceField(
        choices=SCELTA,
        label='Bevi molta acqua?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Bevi molta acqua?'}),
        initial=None,
        error_messages={'required': 'Il campo bevi è obbligatorio.'}
    )

    litri_acqua = forms.FloatField(

        label='Quanti litri al giorno?',
        widget=forms.NumberInput(attrs={
                                 'class': 'form-control font-custom', 'placeholder': 'Quanti litri al giorno?'}),
        error_messages={'required': 'Il campo litri bevuti è obbligatorio.'}
    )

    filosofia_alimentare = forms.ChoiceField(
        choices=ALIMENTAZIONE,
        label='In quale filosofia alimentare ti riconosci?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'In quale filosofia alimentare ti riconosci?'}),
        initial=None,
        error_messages={
            'required': 'Il campo filosofia alimentare è obbligatorio.'}
    )

    maiale = forms.ChoiceField(
        choices=SCELTA,
        label='Mangi carne di Maiale?',
        widget=forms.RadioSelect(attrs={
            'class': 'form-control font-custom', 'placeholder': 'Mangi carne di Maiale?'}),
        initial=None,
        error_messages={'required': 'Il campo mangi maiale è obbligatorio.'}
    )

    figli = forms.ChoiceField(
        choices=SCELTA,
        label='Hai figli?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo figli è obbligatorio.'}
    )

    numero_figli = forms.IntegerField(

        label='Quanti?',
        widget=forms.NumberInput(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Quanti?'}),
        required=False,

    )

    pasto_condiviso = forms.ChoiceField(
        choices=PASTI,
        label='In genere mangiate tutti insieme a?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'In genere mangiate tutti insieme a?'}),
        required=False

    )

    alimenti_preferiti = forms.MultipleChoiceField(
        choices=ALIMENTI,
        label='Alimenti Preferiti',
        widget=forms.CheckboxSelectMultiple(),
    )

    gusti_preferiti = forms.MultipleChoiceField(
        choices=SAPORI,
        label='Gusti Preferiti',
        widget=forms.CheckboxSelectMultiple(),

    )

    patologie = ChoiceFieldNoValidation(
        choices=[],
        label='Disturbi o patologie attuali?',
        widget=forms.CheckboxSelectMultiple(),
        required=False,

    )

    problemi_cardiaci = forms.ChoiceField(
        choices=SCELTA,
        label='Hai o hai avuto problemi cardiaci?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'Hai o hai avuto problemi cardiaci?'}),
        initial=None,
        error_messages={'required': 'Il campo figli è obbligatorio.'}
    )

    problem_cardiaci_tipo = forms.CharField(
        max_length=100,
        label='Tipo di Problemi Cardiaci',
        widget=forms.Textarea(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Quali?'}),
        required=False
    )

    sicura = forms.ChoiceField(
        choices=SCELTA3,
        label='Sei una persona sicura?',
        widget=forms.RadioSelect(attrs={
            'class': 'form-control font-custom', 'placeholder': 'Sei una persona sicura?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    felice = forms.ChoiceField(
        choices=SCELTA3,
        label='Ti senti felice?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    stress = forms.ChoiceField(
        choices=SCELTA3,
        label='Vivi nello stress?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    paure = forms.ChoiceField(
        choices=SCELTA3,
        label='Hai paure o fobie?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    lutti = forms.ChoiceField(
        choices=SCELTA,
        label='Hai avuto lutti recenti?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    incubi = forms.ChoiceField(
        choices=SCELTA3,
        label='Hai spesso incubi?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    stanco = forms.ChoiceField(
        choices=GIORNATA,
        label='Ti senti più stanco?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    rabbia = forms.ChoiceField(
        choices=SCELTA3,
        label='Ti arrabbi spesso?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'id': 'custom_rabbia_id'}),
        error_messages={'required': 'Il campo è obbligatorio.'}

    )

    sfogo = forms.ChoiceField(
        choices=SFOGO,
        label='La rabbia la sfoghi?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    colpa = forms.ChoiceField(
        choices=SCELTA,
        label='Vivi nei sensi di colpa?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    piangi = forms.ChoiceField(
        choices=SCELTA,
        label='Piangi spesso?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Hai figli?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    carattere1 = forms.ChoiceField(
        choices=CAR1,
        label='Sei più?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Sei più?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    carattere2 = forms.ChoiceField(
        choices=CAR2,
        label='Sei più?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Sei più?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    carattere3 = forms.ChoiceField(
        choices=CAR3,
        label='Sei più?',
        widget=forms.RadioSelect(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Sei più?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    determinato = forms.ChoiceField(
        choices=DETERMINATO,
        label='Quanto sei determinato?',
        widget=forms.RadioSelect(attrs={
            'class': 'form-control font-custom', 'placeholder': 'Quanto sei determinato?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'}
    )

    amici_dieta = forms.ChoiceField(
        choices=SCELTA,
        label='Dirai ai tuoi amici o colleghi che sei a dieta?',
        widget=forms.RadioSelect(attrs={'class': 'form-control font-custom',
                                        'placeholder': 'Dirai ai tuoi amici o colleghi che sei a dieta?'}),
        initial=None,
        error_messages={'required': 'Il campo è obbligatorio.'},

    )

    note = forms.CharField(
        max_length=100,
        label='Note',
        widget=forms.Textarea(
            attrs={'class': 'form-control font-custom', 'placeholder': 'Note'}),
        required=False
    )


class AlimentiForm(forms.Form):
    def __init__(self, alimenti, *args, **kwargs):
        super(AlimentiForm, self).__init__(*args, **kwargs)

        for alimento in alimenti:

            self.fields[f'alimento_{alimento["id"]}'] = forms.CharField(

                label=alimento['nome'],
    
                initial=None,
                error_messages={'required': 'Il campo è obbligatorio.'},
            )
