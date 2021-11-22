# Generated by Django 3.2.5 on 2021-11-19 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datasets', '0097_merge_20211116_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
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
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('changelog_id', models.IntegerField(unique=True)),
                ('change_date', models.DateTimeField()),
            ],
            options={'abstract': False},
        ),
        migrations.AlterField(
            model_name='datasetsubscription',
            name='dataset',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='subscriptions',
                to='datasets.dataset',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='datasetsubscription', unique_together={('user', 'dataset')},
        ),
        migrations.CreateModel(
            name='UserNotification',
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
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('email_id', models.UUIDField(null=True)),
                (
                    'notification',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='datasets.notification',
                    ),
                ),
                (
                    'subscription',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='datasets.datasetsubscription',
                    ),
                ),
            ],
            options={'unique_together': {('notification', 'subscription')}},
        ),
    ]