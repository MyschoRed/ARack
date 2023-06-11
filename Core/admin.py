from django.contrib import admin

from Core.models import Palette, Sheet, PaletteSheet

# Register your models here.
admin.site.register(Palette)
admin.site.register(Sheet)
admin.site.register(PaletteSheet)
