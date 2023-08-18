from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse

from Material.models import Sheet
from Rack.forms import SheetToPaletteForm
from Rack.models import PaletteSheet


# Create your views here.
@login_required
def stock(request):
    return render(request, 'Stock/stock.html')



@login_required
def stock_status(request):
    sheets = Sheet.objects.prefetch_related('palettesheet_set').all()

    for sheet in sheets:
        palettes = []
        quantities = []

        for ps in sheet.palettesheet_set.all():
            palettes.append(ps.palette.name)
            quantities.append(ps.quantity)

        sheet.palettes = ', '.join(palettes) if palettes else 'N/A'
        sheet.quantities = ', '.join(map(str, quantities)) if quantities else 'N/A'

    ctx = {
        'sheets': sheets,
    }
    return render(request, 'Stock/stock_status.html', ctx)


@login_required
def stock_palette_edit(request, pk):
    sheet = PaletteSheet.objects.get(pk=pk)
    form = SheetToPaletteForm(instance=sheet)
    ctx = {'sheet': sheet,
           'form': form}
    if request.method == 'GET':
        return render(request, 'Rack/palette_edit.html', ctx)

    if request.method == 'POST':
        data = QueryDict(request.body).dict()
        form = SheetToPaletteForm(data, instance=sheet)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect(reverse('stock_status'))
            # return render(request, 'Core/a_rack.html', ctx)

