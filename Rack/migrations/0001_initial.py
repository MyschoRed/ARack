# Generated by Django 4.2.2 on 2023-08-18 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Palette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=4)),
                ('capacity', models.FloatField()),
                ('load_weight', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Paleta',
                'verbose_name_plural': 'Palety',
            },
        ),
        migrations.CreateModel(
            name='PaletteSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('note', models.CharField(blank=True, max_length=128, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created', to=settings.AUTH_USER_MODEL)),
                ('palette', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Rack.palette')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.sheet')),
            ],
            options={
                'verbose_name': 'Plech na palete',
                'verbose_name_plural': 'Plechy na palete',
            },
        ),
        migrations.AddField(
            model_name='palette',
            name='sheets',
            field=models.ManyToManyField(blank=True, related_name='palette_sheet', through='Rack.PaletteSheet', to='Material.sheet'),
        ),
    ]