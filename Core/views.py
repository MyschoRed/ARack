from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from django.shortcuts import render, redirect

from Core.forms import SheetToPaletteForm, SignUpForm
from Core.models import Palette, PaletteSheet, Sheet


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

# na vytvorenie paliet
def palette_generator():
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


def welcome(request):
    return render(request, 'Core/welcome.html')


@login_required
def stock(request):
    return render(request, 'Core/stock.html')


@login_required
def a_rack(request):
    # palette_generator()
    return render(request, 'Core/a_rack.html')


@login_required
def palette_list(request):
    paletts = Palette.objects.all().order_by('-name')
    palette_color = ''
    ctx = []
    for palette in paletts:
        palette.update_load_weight()
        if palette.load_weight == 0 or palette.load_weight is None:
            palette_color = 'blue'
        elif 0 < palette.load_weight <= 1500:
            palette_color = 'green'
        elif 1500 < palette.load_weight <= palette.capacity:
            palette_color = 'darkorange'
        elif palette.load_weight > palette.capacity:
            palette_color = 'red'
        ctx.append({
            'palette': palette,
            'palette_color': palette_color,
        })
    return render(request, 'Core/palette_list.html', {'pallets': ctx})


@login_required
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


@login_required
def add_sheet_to_palette(request, pk):
    if request.method == 'POST':
        form = SheetToPaletteForm(request.POST or None)
        if form.is_valid():
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
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = SheetToPaletteForm(data, instance=sheet)

        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return render(request, 'Core/palette_detail.html', ctx)


@login_required
def sheet_delete(request, pk):
    sheet = PaletteSheet.objects.get(pk=pk)
    sheet.delete()
    palette = Palette.objects.get(pk=pk)
    palette_sheets = palette.palettesheet_set.all()  # Získanie spojovacej tabuľky pre priradené plechy
    sheets = [sheet for sheet in palette_sheets]
    return render(request, 'Core/palette_detail.html', {'sheets': sheets})


@login_required
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
