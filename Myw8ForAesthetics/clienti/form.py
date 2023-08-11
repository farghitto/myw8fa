from django import forms
from .models import Cliente  # Assicurati di importare il tuo modello


class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cognome', 'citta_nascita', 'data_nascita', 'indirizzo', 'cap',
                  'citta', 'codice_fiscale', 'telefono', 'cellulare', 'email', 'sesso', 'note'
                  ]

        widgets = {'nome': forms.TextInput(
            attrs={'class': "form-control", 'placeholder': 'Nominativo'}), }

        error_messages = {
            'nome': {'required': 'Il nome è obbligatorio.'},
            'cognome': {'required': 'Il cognome è obbligatorio.'},
            'citta_nascita': {'required': 'La città di nascita è obbligatoria.'},
            # ... Aggiungi altri messaggi di errore per i campi
        }
        labels = {
            'nome': 'Nome completo',
            'cognome': 'Cognome completo',
            'citta_nascita': 'Città di nascita',
            # ... Aggiungi altre etichette dei campi
        }
