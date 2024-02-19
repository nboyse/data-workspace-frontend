# Generated by Django 4.2.7 on 2024-02-02 11:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0019_usersatisfactionsurvey_describe_experience_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersatisfactionsurvey",
            name="survey_source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("contact-us", "Contact us"),
                    ("csat-download-link", "CSAT download link"),
                ],
                max_length=32,
                null=True,
            ),
        ),
    ]
