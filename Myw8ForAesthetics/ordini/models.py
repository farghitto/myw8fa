from django.db import models






# Create your models here.
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