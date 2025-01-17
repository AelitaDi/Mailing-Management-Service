# Generated by Django 5.1.4 on 2025-01-17 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mail_service", "0005_alter_mailing_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={
                "ordering": ["email"],
                "permissions": [("can_view_client_list", "Can view client list")],
                "verbose_name": "получатель рассылки",
                "verbose_name_plural": "получатели рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="message",
            options={
                "ordering": ["subject"],
                "permissions": [("can_view_message_list", "Can view message list")],
                "verbose_name": "письмо",
                "verbose_name_plural": "письма",
            },
        ),
    ]