# Generated by Django 3.2.4 on 2021-07-23 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0080_auto_20210611_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetvisualisation',
            name='gds_phase_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]