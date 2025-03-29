from django.core.management import BaseCommand

from mail_service.models import Mailing
from mail_service.services import MailingService


class Command(BaseCommand):
    help_text = 'Команда отправки рассылки через консоль.'

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status='started')

        for mailing in mailings:
            MailingService.send_mailing(mailing.pk)
