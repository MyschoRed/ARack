# Generated by Django 4.2.2 on 2023-08-18 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialSurface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface_name', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'Povrch materialu',
                'verbose_name_plural': 'Povrchy materialu',
            },
        ),
        migrations.CreateModel(
            name='RawMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'Akost materialu',
                'verbose_name_plural': 'Materialove akosti',
            },
        ),
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thickness', models.FloatField()),
                ('size_x', models.IntegerField()),
                ('size_y', models.IntegerField()),
                ('weight', models.FloatField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=128, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material', to='Material.rawmaterial')),
                ('surface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surface', to='Material.materialsurface')),
            ],
            options={
                'verbose_name': 'Plech',
                'verbose_name_plural': 'Plechy',
            },
        ),
    ]
