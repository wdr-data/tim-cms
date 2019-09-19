# Generated by Django 2.2.5 on 2019-09-19 10:36

from django.db import migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0038_auto_20180907_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='media_original',
            field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='Medien-Anhang'),
        ),
        migrations.AlterField(
            model_name='faqfragment',
            name='media_original',
            field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='Medien-Anhang'),
        ),
        migrations.AlterField(
            model_name='push',
            name='media_original',
            field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='Medien-Anhang'),
        ),
        migrations.AlterField(
            model_name='report',
            name='media_original',
            field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='Medien-Anhang'),
        ),
        migrations.AlterField(
            model_name='reportfragment',
            name='media_original',
            field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='Medien-Anhang'),
        ),
        migrations.AlterField(
            model_name='reportquiz',
            name='media_original',
            field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='Medien-Anhang'),
        ),
        migrations.AlterField(
            model_name='wiki',
            name='media_original',
            field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='Medien-Anhang'),
        ),
        migrations.AlterField(
            model_name='wikifragment',
            name='media_original',
            field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='Medien-Anhang'),
        ),
    ]
