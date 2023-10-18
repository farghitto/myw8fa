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
