# Generated by Django 3.2.12 on 2022-04-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0112_pendingauthorizedusers"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pipelineversion",
            name="sql_query",
        ),
        migrations.AddField(
            model_name="pipeline",
            name="config",
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="pipeline",
            name="type",
            field=models.CharField(
                choices=[("sql", "SQL Pipeline"), ("sharepoint", "Sharepoint Pipeline")],
                default="sql",
                max_length=255,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="pipelineversion",
            name="config",
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
