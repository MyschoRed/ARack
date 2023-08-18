from django import forms


from Rack.models import Palette, PaletteSheet


class PaletteForm(forms.ModelForm):
    class Meta:
        model = Palette
        fields = '__all__'


class SheetToPaletteForm(forms.ModelForm):
    class Meta:
        model = PaletteSheet
        fields = '__all__'

