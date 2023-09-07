from django import forms


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
    altezza = forms.FloatField(label='Altezza:',
                               widget=forms.NumberInput(
                                   attrs={'class': 'form-control font-custom', 'placeholder': 'altezza'}),
                               error_messages={'required': 'L\'altezza è obbligatoria.'})
    eta = forms.FloatField(label='Età:',
                           widget=forms.NumberInput(
                               attrs={'class': 'form-control font-custom', 'placeholder': 'eta', 'readonly': True}),
                           error_messages={'required': 'L\'eta è obbligatoria.'})
    bmi = forms.FloatField(label='Bmi:',
                           widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'bmi', 'readonly': True}))
    grasso_corporeo = forms.FloatField(label='Grasso corporeo:', required=False,
                                       widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'grasso_corporeo'}))
    muscolatura = forms.FloatField(label='Muscolatura:', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'muscolatura'}))
    metabolismo = forms.FloatField(label='Metabolismo:', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control font-custom', 'placeholder': 'metabolismo'}))
    grasso_viscerale = forms.FloatField(label='Grasso viscerale:', required=False,
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

    def clean(self):

        cleaned_data = super(FormMisure, self).clean()

        """ ragione_sociale = cleaned_data.get('ragione_sociale')
        sede = cleaned_data.get('sede')
        indirizzo_sede = cleaned_data.get('indirizzo_sede')
        cap_sede = cleaned_data.get('cap_sede')
        partita_iva = cleaned_data.get('partita_iva')
        codice_univoco = cleaned_data.get('codice_univoco')
        
        if ragione_sociale is None:
                self.errors['ragione_sociale'] = ['La ragione sociale è obbligatorio']
        
        if sede is None:
                self.errors['sede'] = ['La città della sede è obbligatorio']
                
        if indirizzo_sede is None:
                self.errors['indirizzo_sede'] = ['L\'indirizzo della sede sociale è obbligatorio']
                
        if partita_iva is None:
                self.errors['partita_iva'] = ['La partita iva è obbligatorio']
                
        if cap_sede is None:
                self.errors['cap_sede'] = ['Il cap della sede sociale è obbligatorio']
                
        if codice_univoco is None:
                self.errors['codice_univoco'] = ['Il codice univoco è obbligatorio']      """

        return cleaned_data
