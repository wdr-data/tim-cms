# Generated by Django 2.0.3 on 2018-09-04 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0030_auto_20180903_1129"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportQuiz",
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
                    "media_original",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="",
                        verbose_name="Medien-Anhang",
                    ),
                ),
                (
                    "media_alt",
                    models.CharField(
                        blank=True,
                        max_length=125,
                        null=True,
                        verbose_name="Alternativ-Text",
                    ),
                ),
                (
                    "media_note",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Credit"
                    ),
                ),
                (
                    "media",
                    models.FileField(
                        blank=True, null=True, upload_to="", verbose_name="Verarbeitet"
                    ),
                ),
                (
                    "quiz",
                    models.BooleanField(
                        default=False,
                        help_text="Diese Meldung ist ein Quiz Element.",
                        verbose_name="Quiz Element",
                    ),
                ),
                (
                    "quiz_option",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="Quiz Option"
                    ),
                ),
                (
                    "quiz_text",
                    models.CharField(max_length=640, verbose_name="Quiz Antwort"),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quiz",
                        related_query_name="quiz",
                        to="cms.Report",
                    ),
                ),
            ],
            options={
                "verbose_name": "Quiz-Fragment",
                "verbose_name_plural": "Quiz-Fragmente",
                "ordering": ("id",),
            },
        ),
    ]
