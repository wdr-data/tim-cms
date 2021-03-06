# Generated by Django 3.1.5 on 2021-01-26 10:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0070_notificationsent"),
    ]

    operations = [
        migrations.CreateModel(
            name="PushCompact",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pub_date",
                    models.DateField(
                        default=datetime.date.today, verbose_name="Push Datum"
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=False,
                        help_text="Solange dieser Haken nicht gesetzt ist, wird dieser Push nicht versendet, auch wenn der konfigurierte Zeitpunkt erreicht wird.",
                        verbose_name="Freigegeben",
                    ),
                ),
                ("intro", models.CharField(max_length=250, verbose_name="Intro-Text")),
                (
                    "outro",
                    models.CharField(
                        help_text="Der Outro-Text schließt den Push ab. Die 👋  wird automatisch hinzugefügt.",
                        max_length=150,
                        verbose_name="Outro-Text",
                    ),
                ),
                (
                    "delivered_fb",
                    models.CharField(
                        choices=[
                            ("not_sent", "nicht gesendet"),
                            ("sending", "wird gesendet"),
                            ("sent", "gesendet"),
                        ],
                        default="not_sent",
                        max_length=20,
                        verbose_name="Facebook",
                    ),
                ),
                (
                    "delivered_date_fb",
                    models.DateTimeField(
                        null=True, verbose_name="Versand-Datum Facebook"
                    ),
                ),
                (
                    "delivered_tg",
                    models.CharField(
                        choices=[
                            ("not_sent", "nicht gesendet"),
                            ("sending", "wird gesendet"),
                            ("sent", "gesendet"),
                        ],
                        default="not_sent",
                        max_length=20,
                        verbose_name="Telegram",
                    ),
                ),
                (
                    "delivered_date_tg",
                    models.DateTimeField(
                        null=True, verbose_name="Versand-Datum Telegram"
                    ),
                ),
                (
                    "attachment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="+",
                        to="cms.attachment",
                        verbose_name="Medien-Anhang",
                    ),
                ),
            ],
            options={
                "verbose_name": "Push",
                "verbose_name_plural": "Morgen-Pushes",
            },
        ),
        migrations.AlterModelOptions(
            name="notificationsent",
            options={"verbose_name": "Empfänger", "verbose_name_plural": "Empfänger"},
        ),
        migrations.AlterModelOptions(
            name="report",
            options={
                "ordering": ["-created"],
                "verbose_name": "Meldung",
                "verbose_name_plural": "Meldungen und Push-Meldungen",
            },
        ),
        migrations.CreateModel(
            name="Teaser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "headline",
                    models.CharField(
                        help_text="Die erste Zeile wird bei Telegram gefettet.",
                        max_length=100,
                        verbose_name="Erste Zeile",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        blank=True,
                        help_text="Dieser Text wird ergänzen gespielt.",
                        max_length=400,
                        verbose_name="Text",
                    ),
                ),
                (
                    "link_name",
                    models.CharField(
                        blank=True,
                        help_text="Hinter diesem Schlagwort wird in TG der Deeplink als Hyperlink gesetzt.",
                        max_length=30,
                        verbose_name="Telegram-Link-Text",
                    ),
                ),
                (
                    "link",
                    models.URLField(
                        blank=True,
                        default=None,
                        help_text="Der Kurz-Link wird nach dem Meldungstext ausgespielt. Bei Telegram als Hyperlink hin dem Telegram-Link-Text. Bei Facebook direkt als Kurz-Link.",
                        max_length=100,
                        verbose_name="Kurz-Link",
                    ),
                ),
                (
                    "push",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teasers",
                        related_query_name="teaser",
                        to="cms.pushcompact",
                    ),
                ),
            ],
            options={
                "verbose_name": "Meldung",
                "verbose_name_plural": "Meldungen",
            },
        ),
        migrations.CreateModel(
            name="Promo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=500, verbose_name="Promo-Text")),
                (
                    "link_name",
                    models.CharField(
                        blank=True, max_length=17, verbose_name="Link-Button-Text"
                    ),
                ),
                (
                    "link",
                    models.URLField(
                        blank=True,
                        default=None,
                        help_text='Der Link wird am Ende am Ende des Promo-Text als Button angehangen. Der Button-Text lautet: "🔗 {Link-Button-Text}".',
                        max_length=500,
                        verbose_name="Link",
                    ),
                ),
                (
                    "attachment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="+",
                        to="cms.attachment",
                        verbose_name="Medien-Anhang",
                    ),
                ),
                (
                    "push",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="promos",
                        related_query_name="promo",
                        to="cms.pushcompact",
                    ),
                ),
            ],
            options={
                "verbose_name": "Promo",
                "verbose_name_plural": "Promos",
            },
        ),
    ]
