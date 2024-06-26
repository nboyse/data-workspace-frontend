# Generated by Django 3.2.19 on 2023-09-01 13:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0150_pipeline_notes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="toolqueryauditlogtable",
            name="schema",
            field=models.CharField(
                db_index=True,
                default="public",
                max_length=63,
                validators=[
                    django.core.validators.RegexValidator(regex="^[a-zA-Z][a-zA-Z0-9_\\.]*$")
                ],
            ),
        ),
        migrations.AlterField(
            model_name="toolqueryauditlogtable",
            name="table",
            field=models.CharField(
                db_index=True,
                max_length=63,
                validators=[
                    django.core.validators.RegexValidator(regex="^[a-zA-Z][a-zA-Z0-9_\\.]*$")
                ],
            ),
        ),
    ]
