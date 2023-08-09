from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from Core.forms import SheetToPaletteForm, SignUpForm, SheetEditForm
from Core.models import Palette, PaletteSheet, Sheet, MaterialIssue


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


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('welcome')
    else:
        form = SignUpForm()
    return render(request, 'Core/registration.html', {'form': form})


def welcome(request):
    return render(request, 'Core/welcome.html')


@login_required
def stock(request):
    return render(request, 'Core/stock.html')


@login_required
def a_rack(request):
    # palette_generator()

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
    return render(request, 'Core/a_rack.html', {'pallets': pallets, 'total_weight': total_weight})


def sheet_list(request):
    all_sheets = Sheet.objects.all()

    ctx = {'all_sheets': all_sheets}
    return render(request, 'Core/sheet_list.html', ctx)


@login_required
def sheet_detail(request, pk):
    sheet = Sheet.objects.get(pk=pk)
    ctx = {
        'sheet': sheet,
    }
    return render(request, 'Core/sheet_detail.html', ctx)


def sheet_edit(request, pk):
    sheet = Sheet.objects.get(pk=pk)
    form = SheetEditForm(instance=sheet)
    ctx = {'sheet': sheet,
           'form': form}
    if request.method == 'GET':
        return render(request, 'Core/sheet_edit.html', ctx)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = SheetEditForm(data, instance=sheet)

        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return render(request, 'Core/sheet_list.html', ctx)


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
    return render(request, 'Core/sheet_add.html', ctx)


@login_required
def sheet_delete(request, pk):
    sheet = Sheet.objects.get(pk=pk)
    sheet.delete()
    palette = Palette.objects.get(pk=pk)
    palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
    sheets = [sheet for sheet in palette_sheets]
    return render(request, 'Core/sheet_detail.html', {'sheets': sheets})


# @login_required
# def palette_list(request):
#     paletts = Palette.objects.all().order_by('-name')
#     palette_color = ''
#     total_weight = 0
#     pallets = []
#     for palette in paletts:
#         palette.update_load_weight()
#         total_weight += palette.load_weight
#         if palette.load_weight == 0 or palette.load_weight is None:
#             palette_color = 'blue'
#         elif 0 < palette.load_weight <= 1500:
#             palette_color = 'green'
#         elif 1500 < palette.load_weight <= palette.capacity:
#             palette_color = 'darkorange'
#         elif palette.load_weight > palette.capacity:
#             palette_color = 'red'
#         pallets.append({
#             'palette': palette,
#             'palette_color': palette_color,
#         })
#
#     return render(request, 'Core/palette_list.html', {'pallets': pallets, 'total_weight': total_weight})


@login_required
def palette_detail(request, pk):
    palette = Palette.objects.get(pk=pk)
    palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
    sheets = [sheet for sheet in palette_sheets]

    ctx = {
        'palette': palette,
        'sheets': sheets,
    }
    return render(request, 'Core/palette_detail.html', ctx)


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
    return render(request, 'Core/add_sheet_to_palette.html', {'form': form, 'palette_id': pk})


@login_required
def palette_edit(request, pk):
    sheet = PaletteSheet.objects.get(pk=pk)
    form = SheetToPaletteForm(instance=sheet)
    ctx = {'sheet': sheet,
           'form': form}
    if request.method == 'GET':
        return render(request, 'Core/palette_edit.html', ctx)

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
    return render(request, 'Core/palette_detail.html', {'sheets': sheets})


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
    return render(request, 'Core/stock_status.html', ctx)


@login_required
def material_issue_list(request):
    all_issues = MaterialIssue.objects.all()
    sheets = PaletteSheet.objects.all()
    ctx = {
        'all_issues': all_issues,
        'sheets': sheets
    }
    return render(request, 'Core/material_issue_list.html', ctx)
