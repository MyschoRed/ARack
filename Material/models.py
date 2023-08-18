from django.db import models

# from Rack.models import PaletteSheet


# Create your models here.
class RawMaterial(models.Model):
    material_name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.material_name}"

    class Meta:
        verbose_name = "Akost materialu"
        verbose_name_plural = "Materialove akosti"


class MaterialSurface(models.Model):
    surface_name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.surface_name}"

    class Meta:
        verbose_name = "Povrch materialu"
        verbose_name_plural = "Povrchy materialu"


class Sheet(models.Model):
    material = models.ForeignKey(to=RawMaterial, on_delete=models.CASCADE, related_name='material')
    surface = models.ForeignKey(to=MaterialSurface, on_delete=models.CASCADE, related_name='surface')
    thickness = models.FloatField()
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    weight = models.FloatField(null=True, blank=True, )
    note = models.CharField(max_length=128, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.weight = round(((self.size_x * self.size_y) / 1000000) * 8 * self.thickness, 3)
        super().save(*args, **kwargs)

    # @property
    # def palette_name(self):
    #     try:
    #         palette_sheet = PaletteSheet.objects.get(sheet=self)
    #         return palette_sheet.palette.name
    #     except PaletteSheet.DoesNotExist:
    #         return "N/A"

    def __str__(self):
        return f"{self.material.material_name}, {self.surface.surface_name}, {self.thickness}x{self.size_x}x{self.size_y}"

    class Meta:
        verbose_name = "Plech"
        verbose_name_plural = "Plechy"
