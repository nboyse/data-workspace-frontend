# Generated by Django 3.2.14 on 2022-08-04 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("explorer", "0019_delete_chartbuilderchart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="querylog",
            name="state",
            field=models.IntegerField(
                choices=[(0, "Running"), (1, "Failed"), (2, "Complete"), (3, "Cancelled")],
                default=0,
            ),
        ),
    ]
