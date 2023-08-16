from django import forms
from .models import Cliente  # Assicurati di importare il tuo modello


class FormCliente(forms.ModelForm):
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
        }
