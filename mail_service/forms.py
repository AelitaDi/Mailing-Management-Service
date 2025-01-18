from django import forms
from django.forms import BooleanField, DateTimeInput

from mail_service.models import Client, Message, Mailing


class StyleFormMixin:
    """
    Миксин для настройки стилей форм.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания клиента.
    """

    class Meta:
        model = Client
        fields = ('email', 'name', 'comment')

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введите email получателя'
        })

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Введите имя получателя'
        })

        self.fields['comment'].widget.attrs.update({
            'placeholder': 'Введите комментарий'
        })


class MessageForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания сообщения.
    """

    class Meta:
        model = Message
        fields = ('subject', 'message')

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({
            'placeholder': 'Введите тему письма'
        })

        self.fields['message'].widget.attrs.update({
            'placeholder': 'Введите сообщение'
        })


class MailingForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания рассылки.
    """

    class Meta:
        model = Mailing
        fields = ('message', 'clients', 'status', 'start_sending_at', 'end_sending_at')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["end_sending_at"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local", 'class': 'form-control'})
        self.fields["start_sending_at"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local", 'class': 'form-control'})

        if user:
            self.fields['message'].queryset = Message.objects.filter(owner=user)
            self.fields['clients'].queryset = Client.objects.filter(owner=user)
