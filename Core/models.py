from django.db import models


# Create your models here.
class Sheet(models.Model):
    material = models.CharField(max_length=64)
    surface = models.CharField(max_length=32)
    tickness = models.FloatField()
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    weight = models.FloatField(null=True, blank=True, )

    def save(self, *args, **kwargs):
        self.weight = ((self.size_x * self.size_y) / 1000000) * 8 * self.tickness
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.material}, {self.surface}, {self.tickness}mm, {self.size_x}, {self.size_y}, {self.weight}kg"

    class Meta:
        verbose_name = "Plech"
        verbose_name_plural = "Plechy"


class Palette(models.Model):
    name = models.CharField(max_length=4)
    capacity = models.FloatField()
    sheets = models.ManyToManyField(Sheet,blank=True, through='PaletteSheet', related_name='palette_sheet')
    load_weight = models.FloatField(null=True, blank=True)

    def calculate_load_weight(self):
        load_weight = self.palettesheet_set.aggregate(total_weight=models.Sum(models.F('sheet__weight') * models.F('quantity')))['total_weight']
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
    palette = models.ForeignKey(Palette, on_delete=models.CASCADE)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.sheet.material} - {self.quantity}"