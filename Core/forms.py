from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Core.models import Palette, PaletteSheet


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


class PaletteForm(forms.ModelForm):
    class Meta:
        model = Palette
        fields = '__all__'


class SheetToPaletteForm(forms.ModelForm):
    class Meta:
        model = PaletteSheet
        fields = '__all__'
