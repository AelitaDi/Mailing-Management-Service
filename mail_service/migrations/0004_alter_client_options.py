# Generated by Django 5.1.4 on 2025-01-07 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mail_service", "0003_alter_mailing_end_sending_at_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={
                "ordering": ["email"],
                "verbose_name": "получатель рассылки",
                "verbose_name_plural": "получатели рассылки",
            },
        ),
    ]
