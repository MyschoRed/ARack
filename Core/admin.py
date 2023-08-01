from django.contrib import admin

from Core.models import RawMaterial, MaterialSurface, Palette, Sheet, PaletteSheet

# Register your models here.
admin.site.register(RawMaterial)
admin.site.register(MaterialSurface)
admin.site.register(Palette)
admin.site.register(Sheet)
admin.site.register(PaletteSheet)
