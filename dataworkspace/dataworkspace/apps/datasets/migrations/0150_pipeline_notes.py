# Generated by Django 3.2.20 on 2023-08-25 09:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0149_auto_20230726_1416"),
    ]

    operations = [
        migrations.AddField(
            model_name="pipeline",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]
