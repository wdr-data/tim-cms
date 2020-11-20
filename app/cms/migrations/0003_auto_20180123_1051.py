# Generated by Django 2.0.1 on 2018-01-23 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0002_push"),
    ]

    operations = [
        migrations.AlterField(
            model_name="push",
            name="intro",
            field=models.CharField(
                blank=True, max_length=640, verbose_name="Intro-Text"
            ),
        ),
        migrations.AlterField(
            model_name="push",
            name="outro",
            field=models.CharField(
                blank=True, max_length=640, verbose_name="Outro-Text"
            ),
        ),
    ]
