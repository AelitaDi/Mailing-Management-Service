import smtplib

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mail_service.models import Attempt, Mailing


class MailingService:
    """
    Класс для работы с рассылками и создания отчетов.
    """

    @staticmethod
    def send_mailing(pk):
        """
        Функция для отправки рассылки через интерфейс пользователя.
        """

        mailing = Mailing.objects.get(pk=pk)
        subject = mailing.message.subject
        message = mailing.message.message
        clients = [client.email for client in mailing.clients.all()]

        start_at = timezone.now()

        try:
            response = send_mail(subject, message, EMAIL_HOST_USER, clients, fail_silently=False)
        except smtplib.SMTPException as e:
            MailingService.log_attempt(status="failure", response=e, mailing=mailing)
        else:
            end_at = timezone.now()
            MailingService.log_attempt(status="success", response=response, mailing=mailing)
            MailingService.update_mailing_status(mailing=mailing, start_at=start_at, end_at=end_at)
        finally:
            return redirect(reverse("mail_service:mailing_list"))

    @staticmethod
    def log_attempt(status, response, mailing):
        """
        Функция для создания записи о попытке рассылки.
        """
        attempt = Attempt.objects.create(status=status, mail_response=response,
                                         mailing=mailing)
        attempt.save()

    @staticmethod
    def update_mailing_status(mailing, start_at, end_at):
        """
        Функция обновления сведений о рассылке.
        """
        mailing.start_sending_at = start_at
        mailing.end_sending_at = end_at
        mailing.status = 'completed'
        mailing.save()
