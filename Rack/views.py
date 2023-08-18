from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse

from Rack.forms import SheetToPaletteForm
from Rack.models import Palette, PaletteSheet


def palette_generator():
    """
    Na vytvorenie paliet
    """
    for i in range(0, 24):
        if i < 9:
            Palette.objects.create(name=f'A0{i + 1}', capacity=2000).save()
        else:
            Palette.objects.create(name=f'A{i + 1}', capacity=2000).save()

    for i in range(0, 24):
        if i < 9:
            Palette.objects.create(name=f'B0{i + 1}', capacity=2000).save()
        else:
            Palette.objects.create(name=f'B{i + 1}', capacity=2000).save()


# Create your views here.
@login_required
def a_rack(request):
    # palette_generator()  # zapnut iba pri inicializacii databazy!!!
    paletts = Palette.objects.all().order_by('-name')

    palette_color = ''
    total_weight = 0
    pallets = []
    for palette in paletts:
        palette.update_load_weight()
        total_weight += palette.load_weight
        if palette.load_weight == 0 or palette.load_weight is None:
            palette_color = 'blue'
        elif 0 < palette.load_weight <= 1500:
            palette_color = 'green'
        elif 1500 < palette.load_weight <= palette.capacity:
            palette_color = 'darkorange'
        elif palette.load_weight > palette.capacity:
            palette_color = 'red'
        pallets.append({
            'palette': palette,
            'palette_color': palette_color,
        })
    return render(request, 'Rack/a_rack.html', {'pallets': pallets, 'total_weight': total_weight})


@login_required
def palette_detail(request, pk):
    palette = Palette.objects.get(pk=pk)
    palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
    sheets = [sheet for sheet in palette_sheets]

    ctx = {
        'palette': palette,
        'sheets': sheets,
    }
    return render(request, 'Rack/palette_detail.html', ctx)


@login_required
def add_sheet_to_palette(request, pk):
    if request.method == 'POST':
        palette = Palette.objects.get(pk=pk)
        palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
        sheets = [sheet.sheet for sheet in palette_sheets]

        form = SheetToPaletteForm(request.POST or None)

        if form.is_valid():
            sheet_is_loaded = form.cleaned_data['sheet']
            if sheet_is_loaded in sheets:
                messages.error(request, f"Tabula {sheet_is_loaded} uz je na palete.")
                # return redirect('errors')
            else:
                palette = Palette.objects.get(pk=pk)
                sheet = form.save(commit=False)
                sheet.palette = palette
                sheet.created_by = request.user
                sheet.save()
                return redirect('palette_detail', pk=palette.pk)
    else:
        form = SheetToPaletteForm()
    return render(request, 'Rack/add_sheet_to_palette.html', {'form': form, 'palette_id': pk})


@login_required
def palette_edit(request, pk):
    sheet = PaletteSheet.objects.get(pk=pk)
    form = SheetToPaletteForm(instance=sheet)
    ctx = {'sheet': sheet,
           'form': form}
    if request.method == 'GET':
        return render(request, 'Rack/palette_edit.html', ctx)

    if request.method == 'POST':
        data = QueryDict(request.body).dict()
        form = SheetToPaletteForm(data, instance=sheet)
        palette = sheet.palette.pk
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect(reverse('palette_detail', args=[palette]))
            # return render(request, 'Core/a_rack.html', ctx)


@login_required
def sheet_on_palette_delete(request, pk):
    sheet = PaletteSheet.objects.get(pk=pk)
    sheet.delete()
    palette = Palette.objects.get(pk=pk)
    palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
    sheets = [sheet for sheet in palette_sheets]
    return render(request, 'Rack/palette_detail.html', {'sheets': sheets})
