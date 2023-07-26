
from django.db.models import Subquery, OuterRef, Prefetch,Count
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404, redirect

from Core.forms import PaletteForm, SheetToPaletteForm
from Core.models import Palette, PaletteSheet, Sheet

from django.contrib.postgres.aggregates import ArrayAgg

# Create your views here.
def home(request):
    return render(request, 'Core/home.html')


def palette_list(request):
    paletts = Palette.objects.all().order_by('-name')
    palette_color = ''
    ctx = []
    for palette in paletts:
        palette.update_load_weight()
        if palette.load_weight == 0 or palette.load_weight is None:
            palette_color = 'blue'
        elif palette.load_weight > 0 and palette.load_weight <= 1500:
            palette_color = 'green'
        elif palette.load_weight > 1500 and palette.load_weight <= palette.capacity:
            palette_color = 'darkorange'
        elif palette.load_weight > palette.capacity:
            palette_color = 'red'
        ctx.append({
            'palette': palette,
            'palette_color': palette_color,
        })
    return render(request, 'Core/palette_list.html', {'pallets': ctx})


def palette_detail(request, pk):
    palette = Palette.objects.get(pk=pk)
    palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
    sheets = [sheet for sheet in palette_sheets]
    load_weight = palette.update_load_weight()

    ctx = {
        'palette': palette,
        'sheets': sheets,
        'load_weight': load_weight
    }
    return render(request, 'Core/palette_detail.html', ctx)


def add_sheet_to_palette(request, pk):
    if request.method == 'POST':
        form = SheetToPaletteForm(request.POST or None)
        if form.is_valid():
            palette = Palette.objects.get(pk=pk)
            print(palette)
            sheet = form.save(commit=False)
            sheet.palette = palette
            sheet.save()
            return redirect('palette_detail', pk=palette.pk)
    else:
        form = SheetToPaletteForm()
    return render(request, 'Core/add_sheet_to_palette.html', {'form': form, 'palette_id': pk})


def palette_edit(request, pk):
    sheet = PaletteSheet.objects.get(pk=pk)
    form = SheetToPaletteForm(instance=sheet)
    ctx = {'sheet': sheet,
           'form': form}
    if request.method == 'GET':
        return render(request, 'Core/palette_edit.html', ctx)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = SheetToPaletteForm(data, instance=sheet)
        if form.is_valid():
            form.save()
            return render(request, 'Core/palette_detail.html', ctx)

def sheet_delete(request, pk):
    sheet = PaletteSheet.objects.get(pk=pk)
    sheet.delete()
    palette = Palette.objects.get(pk=pk)
    palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
    sheets = [sheet for sheet in palette_sheets]
    return render(request, 'Core/palette_detail.html', {'sheets': sheets})


def sheet_list(request):
    sheets = Sheet.objects.prefetch_related('palettesheet_set').all()

    for sheet in sheets:
        palettes = []
        quantities = []

        for ps in sheet.palettesheet_set.all():
            palettes.append(ps.palette.name)
            quantities.append(ps.quantity)

        sheet.palettes = ', '.join(palettes) if palettes else 'N/A'
        sheet.quantities = ', '.join(map(str, quantities)) if quantities else 'N/A'

    # sheets = Sheet.objects.annotate(
    #     palette_name=Subquery(
    #         PaletteSheet.objects.filter(sheet=OuterRef('pk')).values('palette__name')[:1]
    #     ),
    #     quantity_on_palette=Subquery(
    #         PaletteSheet.objects.filter(sheet=OuterRef('pk')).values('quantity')[:1]
    #     )
    # ).values(
    #     'material', 'surface', 'tickness', 'size_x', 'size_y', 'weight', 'palette_name', 'quantity_on_palette'
    # )
    ctx = {
        'sheets': sheets,
    }
    return render(request, 'Core/sheet_list.html', ctx)
