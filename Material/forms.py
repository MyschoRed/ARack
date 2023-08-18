from django import forms

from Material.models import Sheet


class SheetEditForm(forms.ModelForm):
    class Meta:
        model = Sheet
        fields = '__all__'
