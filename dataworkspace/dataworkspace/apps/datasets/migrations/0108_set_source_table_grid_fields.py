# Generated by Django 3.2.11 on 2022-01-28 11:00

from django.db import migrations


def set_download_limit(apps, schema_editor):
    for source in apps.get_model("datasets", "SourceTable").objects.filter(data_grid_enabled=True):
        source.data_grid_download_enabled = (
            source.data_grid_column_config
            and source.data_grid_column_config.get("download_enabled", False)
        )
        if source.data_grid_download_enabled:
            source.data_grid_download_limit = (
                source.data_grid_column_config.get("download_limit", 5000)
                if source.data_grid_column_config
                else 5000
            )
        source.save()


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0107_add_source_table_grid_fields"),
    ]

    operations = [
        migrations.RunPython(code=set_download_limit, reverse_code=migrations.RunPython.noop)
    ]
