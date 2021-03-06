# Generated by Django 2.0.6 on 2018-06-25 14:33

from django.db import migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0024_auto_20180613_0957"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="wikifragment",
            options={
                "ordering": ("id",),
                "verbose_name": "Wiki-Fragment",
                "verbose_name_plural": "Wiki-Fragmente",
            },
        ),
        migrations.AlterField(
            model_name="push",
            name="reports",
            field=sortedm2m.fields.SortedManyToManyField(
                help_text="Bitte maximal 4 Meldungen auswählen.",
                related_name="pushes",
                to="cms.Report",
                verbose_name="Meldungen",
            ),
        ),
    ]
