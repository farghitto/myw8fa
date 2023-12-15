from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class TipoVoceListino(models.Model):
    nome_voce_listino = models.CharField(max_length=30,blank=False,null=False)
    descrizione_voce_listino = models.CharField(max_length=250,blank=False,null=False)


    def __str__(self):
        return self.nome_voce_listino


    class Meta:
        verbose_name = "Tipo Voce Listino"
        verbose_name_plural = "Tipo Voci Listino"


class GruppoListino(models.Model):
    nome_gruppo = models.CharField(max_length=30,blank=False,null=False)
    descrizione_gruppo = models.CharField(max_length=250,blank=False,null=False)
    voce_listino = models.ForeignKey(TipoVoceListino, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.nome_gruppo

    def get_absolute_url(self):
        return reverse("gruppo_accordo_view", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Gruppo Listino"
        verbose_name_plural = "Gruppi Listino"


class Programmi(models.Model):
    """ Dati Programma """
    nome_programma = models.CharField(max_length=50,blank=False,null=False)
    descrizione_programma = models.CharField(max_length=250,blank=False,null=False)
    descrizione_in_fattura = models.CharField(max_length=250,blank=False,null=False)
    durata_programma = models.IntegerField(blank=True,null=True)
    importo = models.DecimalField(max_digits=7,decimal_places=2)
    fasce_kg = models.CharField(max_length=5,blank=True,null=True)
    validita_per_bilanciamento = models.BooleanField(default=False)
    programma_attivo = models.BooleanField(default=False)
    programma_intero = models.BooleanField(default=False)
    codiceiva = models.ForeignKey(to= 'amministrazione.CodiciIva',on_delete=models.CASCADE)
    listino_dedicato = models.ManyToManyField('consulenti.Struttura', related_name="listino_dedicato", blank=True)
    programma_amministratore = models.BooleanField(default=False)

    """informazioni inserimento"""
    data_creazione = models.DateField(auto_now_add=True)
    data_ultima_modifica = models.DateField(auto_now=True)

    """informazioni listino"""
    voce_listino = models.ForeignKey(TipoVoceListino, on_delete=models.CASCADE,blank=True, null=True)
    gruppo = models.ForeignKey(GruppoListino, on_delete=models.CASCADE,related_name='gruppo', null=True,blank=True)

    def __str__(self):
        return self.nome_programma + "-" + self.descrizione_programma


    class Meta:
        verbose_name = "Programma"
        verbose_name_plural = "Programma"
