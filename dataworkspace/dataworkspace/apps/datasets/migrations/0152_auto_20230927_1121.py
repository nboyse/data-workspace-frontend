# Generated by Django 3.2.20 on 2023-09-27 11:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0151_auto_20230901_1347"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="request_approvers",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=256), null=True, size=None
            ),
        ),
        migrations.AddField(
            model_name="visualisationcatalogueitem",
            name="request_approvers",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=256), null=True, size=None
            ),
        ),
    ]
