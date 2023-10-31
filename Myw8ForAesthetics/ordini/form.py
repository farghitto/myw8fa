from django import forms
from datetime import date


class FormRateale(forms.Form):

    acconto = forms.CharField(label='Acconto:',
                              widget=forms.NumberInput(
                                  attrs={'class': 'form-control font-custom', 'placeholder': 'acconto'}), error_messages={'required': 'l\' acconto è obbligatorio.'})
    rate = forms.CharField(label='Rate:',
                           widget=forms.NumberInput(
                                 attrs={'class': 'form-control font-custom', 'placeholder': 'rate'}), error_messages={'required': 'il numero delle rate è obbligatorio'})
    importo_rata = forms.CharField(label='Importo:',
                                   widget=forms.NumberInput(
                                       attrs={'class': 'form-control font-custom', 'placeholder': 'importo', 'readonly': 'readonly'}), error_messages={'required': 'il numero delle rate è obbligatorio'})
    data_ordine = forms.DateField(label='Data inserimento ordine:',
                                  widget=forms.DateInput(
                                      attrs={'class': 'form-control font-custom', 'type': 'date'}),
                                  error_messages={'required': 'La data è obbligatoria.'}, initial=date.today(), )


class ModuliAggiuntiviForm(forms.Form):


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
    data_nascita = forms.DateField(label='Data di nascita:',
                                   widget=forms.DateInput(
                                       attrs={'class': 'form-control font-custom', 'type': 'date'}),
                                   error_messages={'required': 'La data di nascita è obbligatoria.'})
    indirizzo = forms.CharField(max_length=100, label='Indirizzo di residenza:',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control font-custom', 'placeholder': 'indirizzo'}),
                                error_messages={'required': "L'indirizzo è obbligatorio."})
    citta = forms.CharField(max_length=100, label='Citta:',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control font-custom', 'placeholder': 'citta'}),
                            error_messages={'required': 'La città è obbligatorio.'})
    codice_fiscale = forms.CharField(max_length=16, label='Codice fiscale:',
                                     widget=forms.TextInput(
                                         attrs={'class': 'form-control font-custom', 'placeholder': 'codice_fiscale'}),
                                     error_messages={'required': 'La città è obbligatorio.'})
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
    numero_ordine = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label='Numero di ordine')

    
    def __init__(self, *args, **kwargs):

        super(ModuliAggiuntiviForm,self).__init__(*args, **kwargs)

        self.args = args
        if 'initial' in kwargs:
            sesso = kwargs['initial']['sesso']
        elif 'sesso' in self.args[0] :
            sesso = self.args[0]['sesso']


        else:
            sesso = 'F'

        self.fields['provincia_nascita'].label = 'Provincia di nascita'
        self.fields['stato_nascita'].label = 'Stato di nascita'
        self.fields['struttura_fisica'].label = 'In quale struttura fisica ti riconosci?'
        self.fields['struttura_desiderata'].label = 'Quale struttura ti piacerebbe avere?'
        self.fields['diabete'].label = 'Soffri di diabete?'
        self.fields['rapporto_corpo'].label = 'Hai un buon rapporto con il tuo corpo?'
        self.fields['droghe'].label = 'Fai uso di droghe?'
        self.fields['allergie'].label = 'Soffri di allergie?'
        self.fields['allergie_elenco'].label = 'Quali?'
        self.fields['farmaci'].label = 'Assumi farmaci?'
        self.fields['farmaci_elenco'].label = 'Quali?'
        self.fields['sport'].label = 'Pratichi sport?'
        self.fields['sport_praticato'].label = 'Quali?'
        self.fields['sport_praticato_giorni'].label = 'Quante volte alla settimana?'
        self.fields['gruppo_sanguigno'].label = 'Quale è il tuo gruppo sanguigno?'
        self.fields['insonnia'].label = 'Soffri di insonnia?'
        self.fields['stitichezza'].label = 'Soffri di stitichezza?'
        self.fields['menopausa'].label = 'Sei in menopausa?'
        self.fields['gravidanza'].label = 'Sei incinta?'
        self.fields['mesi_gravidanza'].label = 'Di quanti mesi?'
        self.fields['gruppo_sanguigno'].label = "Qual'è il tuo gruppo sanguigno?"
        self.fields['fumo'].label = 'Fumi?'
        self.fields['numero_sigarette'].label = 'Quante sigarette fumi al giorno?'
        self.fields['delta_numero_sigarette'].label = 'Differenza media nazionale'
        self.fields['fame_nervosa'].label = 'Soffri di fame nervosa?'
        self.fields['tatuaggi'].label = 'Hai tatuaggi?'
        self.fields['gengive'].label = 'Problemi di gengive?'
        self.fields['maiale'].label = 'Mangi carne di Maiale?'
        self.fields['bevi_acqua'].label = 'Bevi molta acqua?'
        self.fields['litri_acqua'].label = 'Quanti litri al giorno?'
        self.fields['filosofia_alimentare'].label = 'In quale filosofia alimentare ti riconosci?'
        self.fields['figli'].label = 'Hai figli?'
        self.fields['numero_figli'].label = 'Quanti?'
        self.fields['pasto_condiviso'].label = 'In genere mangiate tutti insieme a?'
        self.fields['alimenti_preferiti'].label = 'Quali alimenti preferisci assumere?'
        self.fields['gusti_preferiti'].label = 'Quali gusti preferisci?'
        self.fields['patologie'].label = 'Disturbi o patologie attuali?'
        self.fields['problemi_cardiaci'].label = 'Hai o hai avuto problemi cardiaci?'
        self.fields['problem_cardiaci_tipo'].label = 'Quali?'
        self.fields['sicura'].label = 'Sei una persona sicura?'
        self.fields['felice'].label = 'Ti senti felice?'
        self.fields['stress'].label = 'Vivi nello stress?'
        self.fields['paure'].label = 'Hai paure o fobie?'
        self.fields['lutti'].label = 'Hai avuto recenti lutti?'
        self.fields['incubi'].label = 'Hai spesso incubi?'
        self.fields['stanco'].label = 'Ti senti più stanco?'
        self.fields['rabbia'].label = 'Ti arrabbi spesso?'
        self.fields['sfogo'].label = 'La rabbia la sfoghi?'
        self.fields['colpa'].label = 'Vivi nei sensi di colpa?'
        self.fields['piangi'].label = 'Piangi spesso?'
        self.fields['incubi'].label = 'Hai spesso incubi?'
        self.fields['carattere1'].label = 'Sei più?'
        self.fields['carattere2'].label =  'Sei più?'
        self.fields['carattere3'].label =  'Sei più?'
        self.fields['determinato'].label = 'Quanto sei determinato?'
        self.fields['amici_dieta'].label = 'Dirai ai tuoi amici o colleghi che sei a dieta??'



        if sesso == 'M':

            self.fields['patologie'].queryset = PatologieClienti.objects.filter(patologia_sesso__in= ['T', 'U'])


            self.fields['menopausa'].initial =  '0'
            self.fields['gravidanza'].initial = '0'
        else:

            self.fields['patologie'].queryset = PatologieClienti.objects.filter(patologia_sesso__in= ['T', 'D'])


        self.fields['scostamento_peso'].widget.attrs['readonly'] = True
        self.fields['bmi'].widget.attrs['readonly']= True
        self.fields['peso_ottimale'].widget.attrs['readonly']= True
        self.fields['stato_attuale'].widget.attrs['readonly']= True
        self.fields['tipo_diabete'].widget.attrs['disabled'] = True
        self.fields['mesi_gravidanza'].widget.attrs['disabled'] = True
        self.fields['allergie_elenco'].widget.attrs['disabled'] = True
        self.fields['farmaci_elenco'].widget.attrs['disabled'] = True
        self.fields['sport_praticato'].widget.attrs['disabled'] = True
        self.fields['sport_praticato_giorni'].widget.attrs['disabled'] = True
        self.fields['numero_sigarette'].widget.attrs['disabled'] = True
        self.fields['delta_numero_sigarette'].widget.attrs['readonly'] = True
        self.fields['numero_figli'].widget.attrs['disabled'] = True
        self.fields['pasto_condiviso'].widget.attrs['disabled'] = True
        self.fields['problem_cardiaci_tipo'].widget.attrs['disabled'] = True