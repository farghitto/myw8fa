# Generated by Django 4.2.4 on 2023-12-15 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('amministrazione', '0003_initial'),
        ('clienti', '0001_initial'),
        ('consulenti', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messaggi_interni',
            name='utente_destinazione',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinatario', to='consulenti.anagraficaconsulente'),
        ),
        migrations.AddField(
            model_name='messaggi_interni',
            name='utente_mittente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mittente', to='consulenti.anagraficaconsulente'),
        ),
        migrations.AddField(
            model_name='indirizziclienti',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clienti.anagraficacliente'),
        ),
        migrations.AddField(
            model_name='gusticlienti',
            name='alimento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amministrazione.alimenti'),
        ),
        migrations.AddField(
            model_name='gusticlienti',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clienti.anagraficacliente'),
        ),
        migrations.AddField(
            model_name='datibiometricicliente',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clienti.anagraficacliente'),
        ),
        migrations.AddField(
            model_name='datibiometricicliente',
            name='dato_biometrico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clienti.datibiometrici'),
        ),
        migrations.AddField(
            model_name='anagraficaclientedati',
            name='cliente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='clienti.anagraficacliente'),
        ),
        migrations.AddField(
            model_name='anagraficaclientedati',
            name='patologie',
            field=models.ManyToManyField(blank=True, null=True, to='clienti.patologieclienti'),
        ),
        migrations.AddField(
            model_name='anagraficacliente',
            name='consulente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='consulenti.anagraficaconsulente'),
        ),
    ]
