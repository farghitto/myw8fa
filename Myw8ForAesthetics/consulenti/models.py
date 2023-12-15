from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from accordi.models import Programmi
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# Create your models here.

class RegimiFiscali(models.Model):

    nome_regime = models.CharField(max_length=20)
    descrizione = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.nome_regime

    class Meta:
        verbose_name = "Regime Fiscale"
        verbose_name_plural = "Regimi Fiscali"


class Struttura(models.Model):

    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Struttura Consulente"


class RuoliConsulente(models.Model):


    ruolo = models.CharField(max_length=40,null=True,blank=True)
    proviggione_unica = models.BooleanField(default=True)
    percorso  = models.ManyToManyField(Struttura,null=True,blank=True)
    visibile = models.ManyToManyField(Group, default="Consulenti")


    def __str__(self):
        return self.ruolo

    class Meta:
        verbose_name = "Ruolo Consulente"
        verbose_name_plural = "Ruoli Consulenti"



class AnagraficaConsulente(models.Model):

    Livelli = (

        (0, '-------'),
        (1, 'Manager'),
        (2, 'Top Manager'),
        (3, 'Silver Manager'),
        (4, 'Gold Manager'),
        (5, 'Platinum Manager')

        )

    #rapporto uno a uno con User
    utente= models.OneToOneField(User, null=True, blank=True,related_name='utente',on_delete=models.CASCADE)
    """ Dati Consulente """
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    luogo_di_nascita = models.CharField(max_length=50)
    provincia_di_nascita =models.CharField(max_length=2)
    data_nascita = models.DateField()
    codice_fiscale = models.CharField(max_length=16)
    indirizzo = models.CharField(max_length=100)
    numero_civico= models.CharField(max_length=5, null=True)
    cap = models.CharField(max_length=5)
    citta_di_residenza = models.CharField(max_length=25)
    provincia_di_residenza =models.CharField(max_length=2)
    regione_residenza = models.CharField(max_length=30)
    stato_residenza = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15,blank=True,null=True)
    cellulare = models.CharField(max_length=15)
    email = models.EmailField(max_length=150)
    banca_appoggio = models.CharField(max_length=100)
    iban = models.CharField(max_length=30)
    note = models.TextField(blank=True,null=True)

    """ Struttura """
    tipo_struttura = models.ForeignKey(Struttura,on_delete=models.SET_NULL,null=True,blank=True)
    id_superiore = models.ForeignKey("self", on_delete=models.SET("senza superiore"),null=True,blank=True)
    """ Questionario informativo fisco """
    ruolo_altra_azienda = models.BooleanField(default=False)
    imponibile_provvigionale = models.FloatField(null=True,blank=True)
    imponibile_provvigionale_parole = models.CharField(max_length=11,default="",null=True,blank=True)
    partita_iva_ateco = models.BooleanField(default=False)
    partita_iva = models.CharField(max_length=11,default="",null=True,blank=True)
    gestione_separata_inps = models.BooleanField(default=False)
    regime = models.ForeignKey(RegimiFiscali,on_delete=models.CASCADE)
    """ date modifica """
    data_creazione = models.DateTimeField(auto_now_add=True)
    data_ultima_modifica = models.DateTimeField(auto_now_add=True)
    """Tipo Consulente"""
    tipo_consulente = models.ForeignKey(RuoliConsulente,on_delete=models.SET_NULL,null=True,blank=True)
    livello_consulente = models.IntegerField(choices=Livelli, default=0)
    beauty_specialist = models.BooleanField(default=False)
    """ Informazioni Tesserino"""
    data_tesserino = models.DateField(null=True,blank=True)
    numero_tesserino = models.IntegerField(null=True,blank=True)
    numero_IVD = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.cognome + " " + self.nome

    class Meta:
        verbose_name = "Consulente"
        verbose_name_plural = "Consulenti"
        
    def get_daticentro(self):
       try:
          return self.datiaggiuntivicentro
       except:
          return None

class DatiAggiuntiviPartner(models.Model):

    consulente= models.OneToOneField(AnagraficaConsulente, null=True, blank=True,related_name='consulente',on_delete=models.CASCADE)
    valore = models.CharField(max_length=10)
    percentuale = models.BooleanField(default=False)
    rete = models.CharField(max_length=50)
    stato = models.BooleanField(default=True)
    data_creazione = models.DateTimeField(auto_now_add=True)
    data_modifica_stato = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.consulente)

    class Meta:
        verbose_name = "Dati Aggiuntivi Partner"
        verbose_name_plural = "Dati Aggiuntivi Partner"

class FormulaCentro(models.Model):

    nome = models.CharField(max_length=20)
    prezzo = models.CharField(max_length=10)
    premio = models.FloatField()

    def __str__(self):
        return str(self.nome)


class DatiAggiuntiviCentro(models.Model):

    Titolare = (


        (1, 'Centro Benessere/Estetico'),
        (2, 'Palestra/Personal Trainer'),
        (3, 'Studio Specialista'),

        )

    CORNER_CHOICES = ((True, 'Corner'), (False, 'Centro Autorizzato'))
    PAGAMENTO_CHOICES = ((True, 'Unica Soluzione'), (False, 'Rateizzato'))

    consulente= models.OneToOneField(AnagraficaConsulente, null=True, blank=True,related_name='corner',on_delete=models.CASCADE)
    corner = models.BooleanField(choices=CORNER_CHOICES,default=False)
    titolare_di = models.IntegerField(choices=Titolare, default=1)
    denominato = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=100)
    cap = models.CharField(max_length=10)
    comune = models.CharField(max_length=30)
    provincia = models.CharField(max_length=10)
    PICF = models.CharField(max_length=50)
    numero_accordo = models.ForeignKey(to= 'amministrazione.AccordoNumeroCorner', on_delete=models.PROTECT,null=True, blank=True)
    formula_scelta = models.ForeignKey(to='FormulaCentro',on_delete=models.CASCADE,null=True,blank=True)
    pagamento = models.BooleanField(choices=PAGAMENTO_CHOICES,default=False)
    affiliatore = models.ForeignKey(to='AnagraficaConsulente',on_delete=models.SET_NULL,null=True,blank=True, related_name='affiliatore')
    seguito = models.ForeignKey(to='AnagraficaConsulente',on_delete=models.SET_NULL,null=True,blank=True, related_name='seguito')

    def __str__(self):
        return str(self.denominato)

class FileCaricatiConsulente(models.Model):

    tipo_file = models.ForeignKey(to= 'amministrazione.FileCaricabili',on_delete=models.CASCADE,null=True,blank=True)
    consulente = models.ForeignKey(AnagraficaConsulente,on_delete=models.CASCADE,null=True,blank=True)
    percorso = models.CharField(max_length=100)
    data_caricamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.tipo_file)

    class Meta:
        verbose_name = "File Caricato"
        verbose_name_plural = "File Caricati"

class ProvvigioniConsulenti(models.Model):

    consulente = models.ForeignKey(AnagraficaConsulente,on_delete=models.CASCADE)
    importo = models.DecimalField(max_digits=9,decimal_places=2)
    ordine =  models.ForeignKey(to= 'amministrazione.Ordine', on_delete=models.CASCADE, null= True, blank=True)
    data_inserimento_ordine = models.DateField()
    data_pagamento_ordine = models.DateField()
    ordine_rateale =  models.BooleanField(default=False)
    rata =  models.CharField(max_length=100,null=True,blank=True)
    provvigione_da_elaragire = models.BooleanField(default=False)
    note = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return "Provvigione Ordine" +str(self.ordine) +  " di " + str(self.consulente)

    class Meta:
        verbose_name = "Provvigione Consulente"
        verbose_name_plural = "Provvigioni Consulenti"

class NotuleConsulenti(models.Model):

    consulente = models.ForeignKey(AnagraficaConsulente,on_delete=models.CASCADE)
    numero = models.CharField(max_length=100, null=True,blank=True)
    dataemissione = models.DateField(default=date.today)
    bloccata = models.BooleanField(default = False)
    datariferimento = models.DateField(default=date.today)

    def __str__(self):
        return "Notula numero" +str(self.numero) +  " di " + str(self.consulente)

    class Meta:
        verbose_name = "Notula Consulente"
        verbose_name_plural = "Notule Consulenti"

