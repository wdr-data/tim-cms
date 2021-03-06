# Generated by Django 2.2.5 on 2019-09-24 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0043_auto_20190924_1431"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="report",
            options={
                "ordering": ["-created"],
                "verbose_name": "Meldung",
                "verbose_name_plural": "Meldungen und Eilmeldungen",
            },
        ),
        migrations.AlterField(
            model_name="push",
            name="timing",
            field=models.CharField(
                choices=[
                    ("morning", "🌇 Morgen"),
                    ("evening", "🌆 Abend"),
                    ("breaking", "🚨 Breaking"),
                    ("testing", "⚗️ Test"),
                ],
                default="morning",
                max_length=20,
                verbose_name="Zeitpunkt",
            ),
        ),
    ]
