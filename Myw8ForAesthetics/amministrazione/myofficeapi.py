



def crea_cliente_myoffice (dati):
    
    indirizzo = dati['indirizzo']
    
    return True



# dati = {
#                 'nome': form.cleaned_data['nome'],
#                 'cognome': form.cleaned_data['cognome'],
#                 'citta_nascita': form.cleaned_data['citta_nascita'],
#               
#                 'data_nascita': form.cleaned_data['data_nascita'],
#                 'indirizzo': form.cleaned_data['indirizzo'], 
#           manca numero_civico

#                 'cap': form.cleaned_data['cap'],
#                 'citta': form.cleaned_data['citta'],
#                 'codice_fiscale': form.cleaned_data['codice_fiscale'],
#                 'telefono': form.cleaned_data['telefono'],
#                 'cellulare': form.cleaned_data['cellulare'],
#                 'email': form.cleaned_data['email'],
#                 'sesso': form.cleaned_data['sesso'],
#                 'note': form.cleaned_data['note'],
#                  consulente rogna devon cercarlo e trovarlo nel database si devono passare
                
#             }

#  

#     """ Consulente """
#     consulente = models.ForeignKey(AnagraficaConsulente, on_delete=models.SET_NULL,null=True)

#     """ Date modifica """
#     data_creazione = models.DateTimeField(auto_now_add=True)
#     data_ultima_modifica = models.DateTimeField(auto_now_add=True)


#     """ Dati Anagrafici Persona Giuridica"""
#     ragione_sociale = models.CharField(max_length=100,null=True,blank=True)
#     sede = models.CharField(max_length=50,blank=True,null=True, default="")
#     indirizzo_sede = models.CharField(max_length=100,null=True,blank=True,default="")
#     cap_sede= models.CharField(max_length=5,null=True,blank=True,default="")
#     telefono_sede = models.CharField(max_length=15,null=True,blank=True,default="")
#     email_sede = models.EmailField(max_length=100,null=True,blank=True,default="")
#     partita_iva = models.CharField(max_length=11,null=True,blank=True)
#     codice_univoco = models.CharField(max_length=8,null=True,blank=True)

#     """Dati Anagrafici Beneficiario"""
#     beneficiario_nome = models.CharField(max_length=50,null=True,blank=True)
#     beneficiario_cognome = models.CharField(max_length=50,null=True,blank=True)
#     beneficiario_cellulare = models.CharField(max_length=15,null=True,blank=True)
#     beneficiario_codice_fiscale = models.CharField(max_length=16,null=True,blank=True)

