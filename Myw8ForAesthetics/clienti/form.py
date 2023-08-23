from django import forms
from .models import Cliente  # Assicurati di importare il tuo modello


""" class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cognome', 'citta_nascita', 'data_nascita', 'indirizzo', 'cap',
                  'citta', 'codice_fiscale', 'telefono', 'cellulare', 'email', 'sesso', 'note'
                  ]

        widgets = {'nome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'nome'}),
                   'cognome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'cognome'}),
                   'citta_nascita': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'citta_nascita'}),
                   'data_nascita': forms.DateInput(attrs={'class': 'form-control font-custom', 'type': 'date'}),
                   'indirizzo': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'indirizzo'}),
                   'cap': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cap'}),
                   'citta': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'citta'}),
                   'codice_fiscale': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'codice_fiscale'}),
                   'telefono': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'telefono'}),
                   'cellulare': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cellulare'}),
                   'email': forms.EmailInput(attrs={'class': "form-control font-custom", 'placeholder': 'email'}),
                   'sesso': forms.Select(choices=[('M', 'M'), ('F', 'F')],attrs={'class': 'form-select font-custom'}),
                   'note': forms.Textarea(attrs={'class': "form-control font-custom", 'placeholder': 'note'}),
                   }
                   

        error_messages = {
            'nome': {'required': 'Il nome è obbligatorio.'},
            'cognome': {'required': 'Il cognome è obbligatorio.'},
            'citta_nascita': {'required': 'La città di nascita è obbligatoria.'},
            'data_nascita': {'required': 'La data di nascita è obbligatoria.'},
            'indirizzo': {'required': "L'indirizzo è obbligatorio."},
            'cap': {'required': 'Il cap è obbligatorio.'},
            'citta': {'required': 'La città è obbligatorio.'},
            'codice_fiscale': {'required': 'Il codice fiscale è obbligatorio.'},
            'cellulare': {'required': 'Il cellulare è obbligatorio.'},
            'email': {'required': "L'email è obbligatoria.", 'invalid': 'L\'indirizzo email non è valido.',},
            'sesso': {'required': 'Il sesso è obbligatorio.'},
            
        }
        labels = {
            'nome': 'Nome:',
            'cognome': 'Cognome:',
            'citta_nascita': 'Città di nascita:',
            'data_nascita': 'Data di nascita:',
            'indirizzo': 'Indirizzo di residenza:',
            'cap': 'Cap:',
            'citta': 'Città:',
            'codice_fiscale': 'Codice fiscale:',
            'telefono': 'Telefono:',
            'cellulare': 'Cellulare:',
            'email': 'Email:',
            'sesso': 'Sesso:',
            'note': 'Note:',
        } """

class FormCliente(forms.Form):
    
    nome = forms.CharField(max_length=100)
    cognome = forms.CharField(max_length=100)
    citta_nascita = forms.CharField(max_length=100)
    data_nascita = forms.DateField()
    indirizzo = forms.CharField(max_length=100)
    cap = forms.CharField(max_length=10)
    citta = forms.CharField(max_length=100)
    codice_fiscale = forms.CharField(max_length=16)
    telefono = forms.CharField(max_length=20)
    cellulare = forms.CharField(max_length=20)
    email = forms.EmailField()
    sesso = forms.ChoiceField(choices=[('M', 'Maschio'), ('F', 'Femmina')])
    note = forms.CharField(widget=forms.Textarea)


    widgets = {'nome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'nome'}),
                'cognome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'cognome'}),
                'citta_nascita': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'citta_nascita'}),
                'data_nascita': forms.DateInput(attrs={'class': 'form-control font-custom', 'type': 'date'}),
                'indirizzo': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'indirizzo'}),
                'cap': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cap'}),
                'citta': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'citta'}),
                'codice_fiscale': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'codice_fiscale'}),
                'telefono': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'telefono'}),
                'cellulare': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cellulare'}),
                'email': forms.EmailInput(attrs={'class': "form-control font-custom", 'placeholder': 'email'}),
                'sesso': forms.Select(choices=[('M', 'M'), ('F', 'F')],attrs={'class': 'form-select font-custom'}),
                'note': forms.Textarea(attrs={'class': "form-control font-custom", 'placeholder': 'note'}),
                }
                   

    error_messages = {
        'nome': {'required': 'Il nome è obbligatorio.'},
        'cognome': {'required': 'Il cognome è obbligatorio.'},
        'citta_nascita': {'required': 'La città di nascita è obbligatoria.'},
        'data_nascita': {'required': 'La data di nascita è obbligatoria.'},
        'indirizzo': {'required': "L'indirizzo è obbligatorio."},
        'cap': {'required': 'Il cap è obbligatorio.'},
        'citta': {'required': 'La città è obbligatorio.'},
        'codice_fiscale': {'required': 'Il codice fiscale è obbligatorio.'},
        'cellulare': {'required': 'Il cellulare è obbligatorio.'},
        'email': {'required': "L'email è obbligatoria.", 'invalid': 'L\'indirizzo email non è valido.',},
        'sesso': {'required': 'Il sesso è obbligatorio.'},
        
    }
    labels = {
        'nome': 'Nome:',
        'cognome': 'Cognome:',
        'citta_nascita': 'Città di nascita:',
        'data_nascita': 'Data di nascita:',
        'indirizzo': 'Indirizzo di residenza:',
        'cap': 'Cap:',
        'citta': 'Città:',
        'codice_fiscale': 'Codice fiscale:',
        'telefono': 'Telefono:',
        'cellulare': 'Cellulare:',
        'email': 'Email:',
        'sesso': 'Sesso:',
        'note': 'Note:',
    }
        
        
        
        


class FormClientePiva(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cognome', 'citta_nascita', 'data_nascita', 'indirizzo', 'cap',
                  'citta', 'codice_fiscale', 'telefono', 'cellulare', 'email', 'sesso', 'note',
                  'ragione_sociale', 'sede', 'indirizzo_sede',  'cap_sede', 'telefono_sede', 
                  'email_sede', 'partita_iva','codice_univoco']
                    

        widgets = {'nome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'nome'}),
                   'cognome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'cognome'}),
                   'citta_nascita': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'citta_nascita'}),
                   'data_nascita': forms.DateInput(attrs={'class': 'form-control font-custom', 'type': 'date'}),
                   'indirizzo': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'indirizzo'}),
                   'cap': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cap'}),
                   'citta': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'citta'}),
                   'codice_fiscale': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'codice_fiscale'}),
                   'telefono': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'telefono'}),
                   'cellulare': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cellulare'}),
                   'email': forms.EmailInput(attrs={'class': "form-control font-custom", 'placeholder': 'email'}),
                   'sesso': forms.Select(choices=[('M', 'M'), ('F', 'F')],attrs={'class': 'form-select font-custom'}),
                   'note': forms.Textarea(attrs={'class': "form-control font-custom", 'placeholder': 'note'}),
                   'ragione_sociale': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'ragione_sociale'}),
                   'sede': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'sede'}),
                   'indirizzo_sede': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'indirizzo_sede'}),
                   'cap_sede': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cap_sede'}),
                   'telefono_sede': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'telefono_sede'}),
                   'email_sede': forms.EmailInput(attrs={'class': "form-control font-custom", 'placeholder': 'email_sede'}),
                   'partita_iva': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'partita_iva'}),
                   'codice_univoco': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'codice_univoco'}),
                   }
                   

        error_messages = {
            'nome': {'required': 'Il nome è obbligatorio.'},
            'cognome': {'required': 'Il cognome è obbligatorio.'},
            'citta_nascita': {'required': 'La città di nascita è obbligatoria.'},
            'data_nascita': {'required': 'La data di nascita è obbligatoria.'},
            'indirizzo': {'required': "L'indirizzo è obbligatorio."},
            'cap': {'required': 'Il cap è obbligatorio.'},
            'citta': {'required': 'La città è obbligatorio.'},
            'codice_fiscale': {'required': 'Il codice fiscale è obbligatorio.'},
            'cellulare': {'required': 'Il cellulare è obbligatorio.'},
            'email': {'required': "L'email è obbligatoria.", 'invalid': 'L\'indirizzo email non è valido.'},
            'sesso': {'required': 'Il sesso è obbligatorio.'},
            'email_sede': {'invalid': 'L\'indirizzo email non è valido.'},          
        }
        
        labels = {
            'nome': 'Nome:',
            'cognome': 'Cognome:',
            'citta_nascita': 'Città di nascita:',
            'data_nascita': 'Data di nascita:',
            'indirizzo': 'Indirizzo di residenza:',
            'cap': 'Cap:',
            'citta': 'Città:',
            'codice_fiscale': 'Codice fiscale:',
            'telefono': 'Telefono:',
            'cellulare': 'Cellulare:',
            'email': 'Email:',
            'sesso': 'Sesso:',
            'note': 'Note:',
            'ragione_sociale': 'Ragione sociale:',
            'sede': 'Sede sociale:',
            'indirizzo_sede': 'Indirizzo sede:',
            'telefono_sede': 'Telefono sede:',
            'cap_sede': 'Cap sede:',
            'email_sede': 'Email sede:',
            'partita_iva': 'Partita iva:',
            'codice_univoco': 'Codice univoco:',         
        }
    
    def clean(self):

        cleaned_data = super(FormClientePiva,self).clean()
        
        ragione_sociale = cleaned_data.get('ragione_sociale')
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
                self.errors['codice_univoco'] = ['Il codice univoco è obbligatorio']     

        return cleaned_data

        

class FormClienteMinore(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cognome', 'citta_nascita', 'data_nascita', 'indirizzo', 'cap',
                  'citta', 'codice_fiscale', 'telefono', 'cellulare', 'email', 'sesso', 'note',
                  'beneficiario_nome', 'beneficiario_cognome', 'beneficiario_cellulare','beneficiario_codice_fiscale']
                    

        widgets = {'nome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'nome'}),
                   'cognome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'cognome'}),
                   'citta_nascita': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'citta_nascita'}),
                   'data_nascita': forms.DateInput(attrs={'class': 'form-control font-custom', 'type': 'date'}),
                   'indirizzo': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'indirizzo'}),
                   'cap': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cap'}),
                   'citta': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'citta'}),
                   'codice_fiscale': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'codice_fiscale'}),
                   'telefono': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'telefono'}),
                   'cellulare': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'cellulare'}),
                   'email': forms.EmailInput(attrs={'class': "form-control font-custom", 'placeholder': 'email'}),
                   'sesso': forms.Select(choices=[('M', 'M'), ('F', 'F')],attrs={'class': 'form-select font-custom'}),
                   'note': forms.Textarea(attrs={'class': "form-control font-custom", 'placeholder': 'note'}),
                   'beneficiario_nome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'beneficiario_nome'}),
                   'beneficiario_cognome': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'beneficiario_cognome'}),
                   'beneficiario_codice_fiscale': forms.TextInput(attrs={'class': "form-control font-custom", 'placeholder': 'indirizzo_sede'}),
                   'beneficiario_cellulare': forms.NumberInput(attrs={'class': "form-control font-custom", 'placeholder': 'beneficiario_cellulare'}),
                   }
                   

        error_messages = {
            'nome': {'required': 'Il nome è obbligatorio.'},
            'cognome': {'required': 'Il cognome è obbligatorio.'},
            'citta_nascita': {'required': 'La città di nascita è obbligatoria.'},
            'data_nascita': {'required': 'La data di nascita è obbligatoria.'},
            'indirizzo': {'required': "L'indirizzo è obbligatorio."},
            'cap': {'required': 'Il cap è obbligatorio.'},
            'citta': {'required': 'La città è obbligatorio.'},
            'codice_fiscale': {'required': 'Il codice fiscale è obbligatorio.'},
            'cellulare': {'required': 'Il cellulare è obbligatorio.'},
            'email': {'required': "L'email è obbligatoria.", 'invalid': 'L\'indirizzo email non è valido.'},
            'sesso': {'required': 'Il sesso è obbligatorio.'},
            'email_sede': {'invalid': 'L\'indirizzo email non è valido.'},          
        }
        
        labels = {
            'nome': 'Nome:',
            'cognome': 'Cognome:',
            'citta_nascita': 'Città di nascita:',
            'data_nascita': 'Data di nascita:',
            'indirizzo': 'Indirizzo di residenza:',
            'cap': 'Cap:',
            'citta': 'Città:',
            'codice_fiscale': 'Codice fiscale:',
            'telefono': 'Telefono:',
            'cellulare': 'Cellulare:',
            'email': 'Email:',
            'sesso': 'Sesso:',
            'note': 'Note:',
            'beneficiario_nome': 'Beneficiario nome:',
            'beneficiario_cognome': 'Beneficiario cognome:',
            'beneficiario_cellulare': 'Beneficiario cellulare',
            'beneficiario_codice_fiscale': 'Beneficiario codice fiscale:',       
        }
        
    def clean(self):

        cleaned_data = super(FormClienteMinore,self).clean()
        
        beneficiario_nome = cleaned_data.get('beneficiario_nome')
        beneficiario_cognome = cleaned_data.get('beneficiario_cognome')
        beneficiario_codice_fiscale = cleaned_data.get('beneficiario_codice_fiscale') 
        print('beneficiario_nome')      
        
        if beneficiario_nome is None:
                self.errors['beneficiario_nome'] = ['Il nome del beneficiario è obbligatorio']
        
        if beneficiario_cognome is None:
                self.errors['beneficiario_cognome'] = ['Il cognome del beneficiario è obbligatorio']
                
        if beneficiario_codice_fiscale is None:
                self.errors['beneficiario_codice_fiscale'] = ['Il codice fiscale del beneficiario è obbligatorio']
                    
        return cleaned_data
        
class ClientiSearchForm(forms.Form):
    
    search_query = forms.CharField(
        label='Cerca:',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control font-custom', 'placeholder': 'Cerca'}),
    )
        
   
    
    