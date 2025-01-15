from django.contrib import admin
from .models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Класс для отображения клиентов в админке.
    """
    search_fields = ('email',)
    list_filter = ('owner',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Класс для отображения сообщений в админке.
    """
    list_filter = ('owner',)
    search_fields = ('subject', 'message',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Класс для отображения рассылок в админке.
    """
    list_filter = ('status',)
    search_fields = ('message',)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    """
    Класс для отображения попыток рассылки в админке.
    """
    list_filter = ('status',)
    search_fields = ('mailing',)
