# Generated by Django 3.1.5 on 2021-04-22 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0077_auto_20210129_1157"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notificationsent",
            name="breaking",
            field=models.BooleanField(verbose_name="🚨 Breaking-Content"),
        ),
        migrations.AlterField(
            model_name="push",
            name="timing",
            field=models.CharField(
                choices=[
                    ("morning", "☕ Morgen"),
                    ("evening", "🌙 Abend"),
                    ("breaking", "🚨 Breaking-Content"),
                    ("testing", "⚗️ Test"),
                ],
                default="morning",
                max_length=20,
                verbose_name="Zeitpunkt",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="delivered_fb",
            field=models.CharField(
                choices=[
                    ("not_sent", "nicht gesendet"),
                    ("sending", "wird gesendet"),
                    ("sent", "gesendet"),
                ],
                default="not_sent",
                max_length=20,
                verbose_name="Breaking-Content/Abend-Push: Facebook",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="delivered_tg",
            field=models.CharField(
                choices=[
                    ("not_sent", "nicht gesendet"),
                    ("sending", "wird gesendet"),
                    ("sent", "gesendet"),
                ],
                default="not_sent",
                max_length=20,
                verbose_name="Breaking-Content/Abend-Push: Telegram",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="type",
            field=models.CharField(
                choices=[
                    ("regular", "📰 Reguläre Meldung"),
                    ("last", "🎨 Letzte Meldung"),
                    ("breaking", "🚨 Breaking-Content"),
                    ("evening", "🌙 Abend-Push"),
                    ("notification", "📨 Benachrichtigung"),
                ],
                default="evening",
                help_text='Wird dieser Wert auf "Breaking-Content", "Abend-Push" oder "Benachrichtigung" gesetzt und die Meldung freigegeben, kann sie direkt versendet werden.',
                max_length=20,
            ),
        ),
    ]
