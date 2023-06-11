# Generated by Django 4.2.2 on 2023-06-10 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="palette",
            name="load_weight",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="palette",
            name="capacity",
            field=models.FloatField(),
        ),
    ]