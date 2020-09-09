# Generated by Django 3.0.8 on 2020-09-08 11:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0051_auto_20200819_0817'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomDatasetQueryTable',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'table',
                    models.CharField(
                        max_length=1024,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex='^[a-zA-Z][a-zA-Z0-9_\\.]*$'
                            )
                        ],
                    ),
                ),
                (
                    'schema',
                    models.CharField(
                        default='public',
                        max_length=1024,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex='^[a-zA-Z][a-zA-Z0-9_\\.]*$'
                            )
                        ],
                    ),
                ),
                (
                    'query',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='tables',
                        to='datasets.CustomDatasetQuery',
                    ),
                ),
            ],
        ),
    ]