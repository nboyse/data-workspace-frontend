# Generated by Django 3.2.19 on 2023-05-16 13:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_migrate_auth_user_model"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dataworkspaceuser",
            options={"verbose_name": "User"},
        ),
    ]
