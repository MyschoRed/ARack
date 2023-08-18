from django.contrib import admin

from IssueNote.models import MaterialIssue
from Material.models import RawMaterial, MaterialSurface, Sheet
from Rack.models import Palette, PaletteSheet

# Register your models here.
admin.site.register(RawMaterial)
admin.site.register(MaterialSurface)
admin.site.register(Palette)
admin.site.register(Sheet)
admin.site.register(PaletteSheet)
admin.site.register(MaterialIssue)
