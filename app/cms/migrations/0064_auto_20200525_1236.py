# Generated by Django 2.2.9 on 2020-05-25 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0063_remove_push_headline"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attachment",
            name="title",
            field=models.CharField(max_length=400, verbose_name="Titel"),
        ),
        migrations.AlterField(
            model_name="report",
            name="link",
            field=models.URLField(
                blank=True,
                default=None,
                help_text='Der Link wird am Ende einer Meldung (FB-Messenger und Letzte Meldung) mit dem Button-Text "MEHR 🌍" ausgespielt, respektive als Hyperlink hinter dem Schlagwort-Text nach dem Telegram-Text.',
                max_length=500,
                null=True,
                verbose_name="DeepLink",
            ),
        ),
    ]
