from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Druh(models.Model):
    nazev = models.CharField(max_length=50, verbose_name='Druh zvířete', help_text='Např. pes, kočka, králík')

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Druh'
        verbose_name_plural = 'Druhy'

    def __str__(self):
        return self.nazev


class Utulek(models.Model):
    nazev = models.CharField(max_length=100, verbose_name='Název útulku')
    adresa = models.CharField(max_length=200, verbose_name='Adresa útulku')
    kontakt = models.CharField(max_length=100, verbose_name='Kontakt (telefon/email)')

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Útulek'
        verbose_name_plural = 'Útulky'

    def __str__(self):
        return self.nazev


class Zvire(models.Model):
    jmeno = models.CharField(max_length=80, verbose_name='Jméno zvířete')
    druh = models.ForeignKey(Druh, on_delete=models.CASCADE, verbose_name='Druh')
    vek = models.PositiveIntegerField(validators=[MaxValueValidator(50)], verbose_name='Věk (v letech)')
    popis = models.TextField(blank=True, verbose_name='Popis')
    prijato = models.DateField(verbose_name='Datum přijetí')
    adoptovano = models.BooleanField(default=False, verbose_name='Adoptováno')
    fotografie = models.ImageField(upload_to='zvirata', verbose_name='Fotografie')
    utulek = models.ForeignKey(Utulek, on_delete=models.CASCADE, verbose_name='Útulek')

    plemeno = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Plemeno',
        help_text='Nepovinné plemeno zvířete'
    )

    STAV_ZDRAVI_CHOICES = [
        ('zdravy', 'Zdravý'),
        ('leci_se', 'Léčí se'),
        ('nemocny', 'Nemocný'),
    ]

    stav_zdravi = models.CharField(
        max_length=20,
        choices=STAV_ZDRAVI_CHOICES,
        default='zdravy',
        verbose_name='Stav zdraví'
    )

    class Meta:
        ordering = ['jmeno']
        verbose_name = 'Zvíře'
        verbose_name_plural = 'Zvířata'

    def __str__(self):
        return f'{self.jmeno} ({self.druh})'


class Dotaz(models.Model):
    TYPY = [
        ('zadost_adopce', 'Žádost o adopci'),
        ('dotaz_ke_zvireti', 'Dotaz ke zvířeti'),
        ('schuzka', 'Smluvení schůzky'),
    ]

    email = models.EmailField(verbose_name='Email')
    typ = models.CharField(max_length=50, choices=TYPY, verbose_name='Typ dotazu')
    zvire = models.ForeignKey('Zvire', on_delete=models.CASCADE, verbose_name='Zvíře')
    popis = models.TextField(verbose_name='Popis dotazu')

    def __str__(self):
        return f'Dotaz od {self.email} ohledně {self.zvire.jmeno}'

class ArchivZvire(models.Model):
    zvire = models.OneToOneField(Zvire, on_delete=models.CASCADE, verbose_name='Zvíře')
    datum_adopce = models.DateField(verbose_name='Datum adopce')
    poznamky = models.TextField(blank=True, verbose_name='Poznámky k archivaci')

    class Meta:
        verbose_name = 'Archivované zvíře'
        verbose_name_plural = 'Archivovaná zvířata'

    def __str__(self):
        return f'Archiv: {self.zvire.jmeno} (adoptováno {self.datum_adopce})'
