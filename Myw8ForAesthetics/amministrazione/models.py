from django.db import models
from consulenti.models import AnagraficaConsulente
from accordi.models import Programmi
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
def incremento_accordo():

    ultimo = AccordoNumero.objects.order_by('id').last()
    obj = datetime.now().year
    anno = str(obj)

    if not ultimo:  # aggiungere reset al nuovo anno

        return '0001' + '/' + anno

    numero_ordine = ultimo.numero_accordo
    numero_ordine_intero = int(numero_ordine.split('/')[0])
    new_numero_ordine = numero_ordine_intero + 1
    new_numero_ordine_stringa = str(new_numero_ordine) + '/' + anno

    return new_numero_ordine_stringa


class AccordoNumero(models.Model):

    numero_accordo = models.CharField(
        max_length=10, default=incremento_accordo)
    tipo_accordo = models.CharField(max_length=100)

    def __str__(self):
        return self.numero_accordo

    class Meta:
        verbose_name = "Numero Accordo"
        verbose_name_plural = "Numeri Accordi"


def incremento_accordo_corner():

    ultimo = AccordoNumeroCorner.objects.order_by('id').last()
    obj = datetime.now().year
    anno = str(obj)

    if not ultimo:  # aggiungere reset al nuovo anno

        return '0051'

    numero_ordine = ultimo.numero_accordo
    numero_ordine_intero = int(numero_ordine)
    new_numero_ordine = numero_ordine_intero + 1
    new_numero_ordine_stringa = str(new_numero_ordine)

    return new_numero_ordine_stringa


class AccordoNumeroCorner(models.Model):

    numero_accordo = models.CharField(
        max_length=10, default=incremento_accordo_corner)
    tipo_accordo = models.CharField(max_length=100)

    def __str__(self):
        return self.numero_accordo

    class Meta:
        verbose_name = "Numero Accordo Corner"
        verbose_name_plural = "Numeri Accordi Corner"


class Ordine(models.Model):

    MODALITA = (

        ('Integrale', 'Saldo Immediato'),
        ('Rateale', 'Pagamento Rateale'),
        ('Finanziato', 'Pagamento attraverso finanziaria')
    )

    STATO = (

        ('Inserito', 'Inserito nel sistema'),
        ('Attesa', 'Attesa del Pagamento'),
        ('Attivato', 'Ordine in lavorazione'),
        ('Sospeso', 'Ordine Sospeso')
    )

    cliente = models.ForeignKey(
        to='clienti.AnagraficaCliente', on_delete=models.PROTECT)
    consulente = models.ForeignKey(
        AnagraficaConsulente, on_delete=models.PROTECT)
    numero_ordine = models.ForeignKey(AccordoNumero, on_delete=models.PROTECT)
    utente_inserimento = models.ForeignKey(User, on_delete=models.PROTECT)
    validita_per_bilanciamento = models.BooleanField(
        default=False, null=True, blank=True)
    """Indirizzo Spedizione"""
    indirizzo = models.CharField(max_length=100)
    numero_civico = models.CharField(max_length=5, null=True)
    cap = models.CharField(max_length=5)
    citta = models.CharField(max_length=25)

    """ Date """
    data_creazione = models.DateTimeField()
    data_ultima_modifica = models.DateTimeField(blank=True, null=True)
    utente_ultima_modifica = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='utente_modifica', blank=True, null=True)
    data_pagamento_ordine = models.DateField(blank=True, null=True)
    """ Pagamenti """
    modalita_pagamento = models.CharField(max_length=50, choices=MODALITA)
    importo_acconto = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    numero_rate = models.IntegerField(blank=True, null=True)
    mesi_tra_le_rate = models.IntegerField(blank=True, null=True)
    importo_rata = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)

    """ Stato Ordine"""

    stato_ordine = models.CharField(max_length=50, choices=STATO)

    def __str__(self):
        return str(self.numero_ordine.numero_accordo) + "-" + str(self.cliente)

    class Meta:
        verbose_name = "Ordine"
        verbose_name_plural = "Ordini"


class DettaglioOrdini(models.Model):

    ordine = models.ForeignKey(Ordine, on_delete=models.PROTECT)

    """ Listino """

    chiave_listino = models.CharField(max_length=5, blank=False, null=False)
    nome_listino = models.CharField(max_length=50, blank=False, null=False)
    descrizione_programma = models.CharField(
        max_length=250, blank=False, null=False)
    importo = models.DecimalField(max_digits=10, decimal_places=2)

    """ Prezzo """
    gratuita = models.BooleanField(default=False)
    iva = models.IntegerField(blank=True, null=True)
    imponibile = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.ordine) + self.nome_listino

    class Meta:
        verbose_name = "Dettaglio Ordine"
        verbose_name_plural = "Dettaglio Ordini"


class EmailAzienda(models.Model):

    descrizione = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, blank=True, null=True)
    testo_oggetto = models.CharField(max_length=50)
    testo_mail = models.TextField(blank=True, null=True)
    bcc = models.EmailField(max_length=150, blank=True, null=True)
    bcc2 = models.EmailField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.descrizione

    class Meta:
        verbose_name = "Email Azienda"
        verbose_name_plural = "Email Azienda"


class Costanti(models.Model):

    valore = models.CharField(max_length=20)
    descrizione = models.CharField(max_length=50)

    def __str__(self):
        return self.descrizione

    class Meta:
        verbose_name = "Costante"
        verbose_name_plural = "Costanti"


class FileCaricabili(models.Model):

    tipodifile = models.CharField(max_length=20)
    descrizione = models.CharField(max_length=50)
    profiloutente = models.ForeignKey(
        to='consulenti.RuoliConsulente', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.tipodifile.replace('_', ' ')

    class Meta:
        verbose_name = "File Caricabile"
        verbose_name_plural = "File Caricabili"


class AnagraficaProvvigioni(models.Model):

    tipo_consulente = models.ForeignKey(
        to='consulenti.RuoliConsulente', on_delete=models.CASCADE)
    consulente_partner = models.ForeignKey(
        to='consulenti.AnagraficaConsulente', on_delete=models.CASCADE, null=True, blank=True)
    linea = models.CharField(max_length=3, null=True, blank=True)
    importo_linea = models.CharField(max_length=10, null=True, blank=True)
    percentuale = models.CharField(max_length=3, null=True, blank=True)
    listino = models.ForeignKey(
        to='accordi.Programmi', on_delete=models.CASCADE)
    rete = models.ForeignKey(to='consulenti.Struttura',
                             on_delete=models.CASCADE, default=1)
    data_inizio_validita = models.DateTimeField(null=True, blank=True)
    data_fine_validita = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.listino) + ' ' + str(self.tipo_consulente)

    class Meta:
        verbose_name = "Anagrafica Provvigione"
        verbose_name_plural = "Anagrafica Provvigioni"


class CodiciIva(models.Model):

    nome = models.CharField(max_length=3)
    valore = models.IntegerField()
    descrizione = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Codice Iva"
        verbose_name_plural = "Codici Iva"


class Scadenze(models.Model):

    STATO = (

        ('Pagato', 'Pagamento Inserito'),
        ('Non Pagato', 'In Attesa del Pagamento')
    )

    cliente = models.ForeignKey(
        to='clienti.AnagraficaCliente', on_delete=models.PROTECT)
    consulente = models.ForeignKey(
        AnagraficaConsulente, on_delete=models.PROTECT)
    numero_ordine = models.ForeignKey(AccordoNumero, on_delete=models.PROTECT)

    """ Date modifica """
    data_creazione = models.DateTimeField(auto_now_add=True)
    data_scadenza = models.DateField()
    data_pagamento_ordine = models.DateField(null=True, blank=True)

    """ Pagamenti """
    importo = models.DecimalField(max_digits=9, decimal_places=2)

    """ Stato Ordine"""
    stato_ordine = models.CharField(max_length=20, choices=STATO)

    def __str__(self):
        return str(self.numero_ordine.numero_accordo) + "-" + str(self.data_scadenza) + "-" + self.cliente.cognome

    class Meta:
        verbose_name = "Scadenza"
        verbose_name_plural = "Scadenze"


class Documentazione(models.Model):

    nome_documento = models.CharField(max_length=60, null=True, blank=True)
    descrizione_documento = models.CharField(max_length=30)
    percorso = models.CharField(max_length=100)
    data_caricamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_documento

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documenti"


class Alimenti(models.Model):

    CLASSE = (
        ('Legumi', 'Legumi'),
        ('Latticini', 'Latticini'),
        ('Frutta secca', 'Frutta secca'),
        ('Uovo', 'Uovo'),
        ('Tacchino', 'Tacchino'),
        ('Manzo', 'Manzo'),
        ('Maiale', 'Maiale'),
        ('Coniglio', 'Coniglio'),
        ('Vitello', 'Vitello'),
        ('Agnello', 'Agnello'),
        ('Frutta', 'Frutta'),
        ('Verdura', 'Verdura'),
        ('Pesce', 'Pesce'),
        ('Pollo', 'Pollo'),
        ('Crostacei', 'Crostacei'),
        ('Molluschi', 'Molluschi'),
    )

    nome = models.CharField(max_length=50)
    classe_alimenti = models.CharField(max_length=25, choices=CLASSE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Alimento"
        verbose_name_plural = "Alimenti"
