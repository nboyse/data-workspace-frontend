# Generated by Django 3.2.20 on 2023-08-24 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("applications", "0022_auto_20230531_1549"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="applicationinstance",
            index=models.Index(fields=["state"], name="app_applica_state_9beedf_idx"),
        ),
    ]
