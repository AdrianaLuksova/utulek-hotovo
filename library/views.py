from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django import forms
from .models import Zvire, Dotaz, Druh, Utulek


class ZvireForm(forms.ModelForm):
    class Meta:
        model = Zvire
        fields = '__all__'

def index(request):
    return render(request, 'library/zaklad/index.html')

def seznam_zvirat(request):
    druhy = Druh.objects.all()
    # Zobrazíme pouze zvířata, která nejsou adoptována
    zvirata = Zvire.objects.filter(adoptovano=False)

    druh_id = request.GET.get('druh')
    plemeno = request.GET.get('plemeno')
    vek = request.GET.get('vek')
    stav_zdravi = request.GET.get('stav_zdravi')

    if druh_id:
        try:
            zvirata = zvirata.filter(druh_id=int(druh_id))
        except ValueError:
            pass
    if plemeno:
        zvirata = zvirata.filter(plemeno__icontains=plemeno)
    if vek:
        try:
            zvirata = zvirata.filter(vek=int(vek))
        except ValueError:
            pass
    if stav_zdravi:
        zvirata = zvirata.filter(stav_zdravi=stav_zdravi)

    return render(request, 'library/seznam_zvirat.html', {
        'zvirata': zvirata,
        'druhy': druhy,
        'filtry': {
            'druh': druh_id or '',
            'plemeno': plemeno or '',
            'vek': vek or '',
            'stav_zdravi': stav_zdravi or '',
        }
    })


def kontakt(request):
    zvirata = Zvire.objects.all()

    if request.method == 'POST':
        email = request.POST.get('email')
        typ = request.POST.get('typ')
        zvire_id = request.POST.get('zvire')
        popis = request.POST.get('popis')

        if not all([email, typ, zvire_id, popis]):
            messages.error(request, "Vyplňte, prosím, všechna pole.")
        else:
            Dotaz.objects.create(
                email=email,
                typ=typ,
                zvire_id=int(zvire_id),
                popis=popis
            )
            messages.success(request, "Váš dotaz byl úspěšně odeslán. Děkujeme!")
            return redirect('kontakt')

    return render(request, 'library/kontakt.html', {
        'zvirata': zvirata,
        'typy': Dotaz.TYPY,
    })

def detail_zvirete(request, zvire_id):
    zvire = get_object_or_404(Zvire, id=zvire_id)
    return render(request, 'library/detail_zvirete.html', {'zvire': zvire})

def upravit_zvire(request, zvire_id):
    zvire = get_object_or_404(Zvire, id=zvire_id)
    if request.method == 'POST':
        form = ZvireForm(request.POST, request.FILES, instance=zvire)
        if form.is_valid():
            zvire = form.save()
            messages.success(request, 'Zvíře bylo upraveno.')

            if zvire.adoptovano:
                return redirect('archiv_zvirat')  # Pokud bylo adoptováno, přesměruj do archivu

            return redirect('detail_zvirete', zvire_id=zvire.id)
    else:
        form = ZvireForm(instance=zvire)
    return render(request, 'library/upravit_zvire.html', {'form': form, 'zvire': zvire})


def smazat_zvire(request, zvire_id):
    zvire = get_object_or_404(Zvire, id=zvire_id)

    if request.method == "POST":
        zvire.delete()
        messages.success(request, "Zvíře bylo úspěšně smazáno.")
        return redirect("seznam_zvirat")

    return render(request, "library/smazat_zvire.html", {"zvire": zvire})

def seznam_utulku(request):
    utulky = Utulek.objects.all()
    return render(request, 'library/seznam_utulku.html', {
        'utulky': utulky,
    })

def archiv_zvirat(request):
    archivovana_zvirata = Zvire.objects.filter(adoptovano=True)
    return render(request, 'library/archiv_zvirat.html', {'zvirata': archivovana_zvirata})