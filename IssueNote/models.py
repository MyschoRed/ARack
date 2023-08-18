from django.db import models

from Rack.models import PaletteSheet


# Create your models here.
class MaterialIssue(models.Model):
    """
    Materialova vydajka
    """
    order_number = models.CharField(max_length=64)
    sheets = models.ManyToManyField(to=PaletteSheet, related_name='material_issue_sheet')

    def __str__(self):
        return f"{self.order_number}"

    class Meta:
        verbose_name = "Materialova vydajka"
        verbose_name_plural = "Materialove vydajky"
