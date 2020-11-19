# Generated by Django 3.0.7 on 2020-11-18 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0068_auto_20200917_1954"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="type",
            field=models.CharField(
                choices=[
                    ("regular", "📰 Reguläre Meldung"),
                    ("last", "🎨 Letzte Meldung"),
                    ("breaking", "🚨 Breaking"),
                    ("evening", "🌙 Abend-Push"),
                    ("notification", "📨 Benachrichtigung"),
                ],
                default="regular",
                help_text='Wird dieser Wert auf "Breaking", "Abend-Push" oder "Benachrichtigung" gesetzt und die Meldung freigegeben, kann sie direkt versendet werden.',
                max_length=20,
                verbose_name="Meldungstyp",
            ),
        ),
    ]
