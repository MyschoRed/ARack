from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from django.shortcuts import render, redirect

from Material.forms import SheetEditForm
from Material.models import Sheet
from Rack.models import Palette


# Create your views here.
def sheet_list(request):
    all_sheets = Sheet.objects.all()

    ctx = {'all_sheets': all_sheets}
    return render(request, 'Material/sheet_list.html', ctx)


@login_required
def sheet_detail(request, pk):
    sheet = Sheet.objects.get(pk=pk)
    ctx = {
        'sheet': sheet,
    }
    return render(request, 'Material/sheet_detail.html', ctx)


def sheet_edit(request, pk):
    sheet = Sheet.objects.get(pk=pk)
    form = SheetEditForm(instance=sheet)
    ctx = {'sheet': sheet,
           'form': form}
    if request.method == 'GET':
        return render(request, 'Material/sheet_edit.html', ctx)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = SheetEditForm(data, instance=sheet)

        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return render(request, 'Material/sheet_list.html', ctx)


def sheet_add(request):
    if request.method == 'POST':
        form = SheetEditForm(request.POST or None)
        if form.is_valid():
            sheet = form.save()
            sheet.save()
            return redirect('sheet_list')
    else:
        form = SheetEditForm()

    ctx = {'form': form}
    return render(request, 'Material/sheet_add.html', ctx)


@login_required
def sheet_delete(request, pk):
    sheet = Sheet.objects.get(pk=pk)
    sheet.delete()
    palette = Palette.objects.get(pk=pk)
    palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
    sheets = [sheet for sheet in palette_sheets]
    return render(request, 'Material/sheet_detail.html', {'sheets': sheets})

