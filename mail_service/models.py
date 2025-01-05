from django.db import models

from users.models import User


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(
        max_length=250,
        verbose_name="Ф.И.О.",
        help_text="Введите Ф.И.О. клиента рассылки",
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий",
        help_text="Введите комментарий",
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="client")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "получатель рассылки"
        verbose_name_plural = "получателя рассылки"
        ordering = ["email"]


class Message(models.Model):
    subject = models.CharField(
        max_length=250,
        verbose_name="Тема письма",
        help_text="Введите тему",
    )
    message = models.TextField(
        verbose_name="Сообщение",
        help_text="Введите сообщение",
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="messages")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        ordering = ["subject"]


class Mailing(models.Model):
    COMPLETED = 'completed'
    CREATED = 'created'
    STARTED = 'started'
    STATUS_CHOICES = [
        (COMPLETED, 'Завершена'),
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
    ]
    start_sending_at = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    end_sending_at = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name='Статус рассылки'
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', related_name='mailings')
    clients = models.ManyToManyField(Client, verbose_name='Получатели рассылки',
                                     help_text='Выберите получателей рассылки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="mailing")

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["message", "owner"]


class Attempt(models.Model):
    SUCCESS = 'success'
    FAILURE = 'failure'
    STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILURE, 'Не успешно'),
    ]
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        verbose_name='Статус попытки')
    mail_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', related_name='attempt')

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "попытки"
        ordering = ["created_at"]
