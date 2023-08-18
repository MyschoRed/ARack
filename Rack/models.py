from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from Material.models import Sheet


# Create your models here.

class Palette(models.Model):
    name = models.CharField(max_length=4)
    capacity = models.FloatField()
    sheets = models.ManyToManyField(Sheet, blank=True, through='PaletteSheet', related_name='palette_sheet')
    load_weight = models.FloatField(null=True, blank=True)

    def calculate_load_weight(self):
        load_weight = \
            self.palettesheet_set.aggregate(total_weight=models.Sum(models.F('sheet__weight') * models.F('quantity')))[
                'total_weight']
        self.load_weight = load_weight if load_weight else 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def update_load_weight(self):
        self.calculate_load_weight()
        self.save(update_fields=['load_weight'])

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Paleta"
        verbose_name_plural = "Palety"


class PaletteSheet(models.Model):
    palette = models.ForeignKey(Palette, on_delete=models.CASCADE, null=True, blank=True)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    note = models.CharField(max_length=128, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.palette}: {self.sheet.material}, {self.quantity}ks"

    class Meta:
        verbose_name = "Plech na palete"
        verbose_name_plural = "Plechy na palete"


@receiver(pre_save, sender=PaletteSheet)
def palette_sheet_pre_save(sender, instance, **kwargs):
    if not instance.id:
        instance.created_date = timezone.now()
        instance.created_by = get_user_model().objects.get(username=instance.created_by.username)

