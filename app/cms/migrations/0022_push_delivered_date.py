# Generated by Django 2.0.3 on 2018-03-19 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0021_push_pub_date_refactor"),
    ]

    operations = [
        migrations.AddField(
            model_name="push",
            name="delivered_date",
            field=models.DateTimeField(null=True, verbose_name="Versand-Datum"),
        ),
    ]
