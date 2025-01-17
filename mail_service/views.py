from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from mail_service.forms import ClientForm, MessageForm, MailingForm
from mail_service.models import Client, Mailing, Message, Attempt
from mail_service.services import MailingService


def home_view(request):
    """
    Контроллер для главной страницы.
    """
    mailing_count = Mailing.objects.count()
    started_mailing_count = Mailing.objects.filter(status='started').count()
    clients = Client.objects.count()
    context = {
        'mailing_count': mailing_count,
        'started_mailing_count': started_mailing_count,
        'clients': clients,
    }
    return render(request, 'mail_service/home.html', context)


class StatisticsView(LoginRequiredMixin, TemplateView):
    """
    Класс для отображения статистики по рассылкам.
    """

    template_name = "mail_service/statistics.html"

    def get_context_data(self, **kwargs):
        """
        Добавление параметров в контекст.
        """

        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailings = Mailing.objects.filter(owner=user)
        attempts = Attempt.objects.filter(mailing__in=mailings)
        print(attempts)

        success = 0
        failure = 0
        mail_count = 0

        for attempt in attempts:
            if attempt.status == "success":
                success += 1
                mail_count += attempt.mailing.clients.count()

            else:
                failure += 1
        context['mail_count'] = mail_count
        context['success'] = success
        context['failure'] = failure

        return context


class ClientListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения списка получателей рассылки.
    """
    model = Client

    # paginate_by = 5

    def get_queryset(self):
        """
        Переопределение queryset.
        """
        if not self.request.user.has_perm('can_view_client_list'):
            return MailingService.caching(super().get_queryset(), self.model, self.request.user)
        else:
            return MailingService.caching(super().get_queryset(), self.model)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для отображения данных о получателе рассылки.
    """
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания получателя рассылки.
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail_service:home')

    def form_valid(self, form):
        client = form.save(commit=False)
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования данных получателя рассылки.
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ClientForm
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления получателя рассылки.
    """
    model = Client
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return self.form_class
        raise PermissionDenied

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения списка писем.
    """
    model = Message

    # paginate_by = 5

    def get_queryset(self):
        if not self.request.user.has_perm('can_view_message_list'):
            return MailingService.caching(super().get_queryset(), self.model, self.request.user)
        else:
            return MailingService.caching(super().get_queryset(), self.model)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления письма.
    """
    model = Message
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return self.form_class
        raise PermissionDenied

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        raise PermissionDenied


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для отображения данных письма.
    """
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания письма.
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_service:home')

    def form_valid(self, form):
        message = form.save(commit=False)
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования письма.
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        raise PermissionDenied


class MailingListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения списка рассылок.
    """
    model = Mailing

    # paginate_by = 5

    def get_queryset(self):
        if not self.request.user.has_perm('mail_service.can_finish_mailing'):
            return MailingService.caching(super().get_queryset(), self.model, self.request.user)
        else:
            return MailingService.caching(super().get_queryset(), self.model)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления рассылки.
    """
    model = Mailing
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return self.form_class
        raise PermissionDenied

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        raise PermissionDenied


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для просмотра рассылки.
    """
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания рассылки.
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail_service:home')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        print(form_kwargs['user'])
        return form_kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования рассылки.
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        raise PermissionDenied

    @staticmethod
    def finish_mailing(request, pk):
        finish_mailing = Mailing.objects.get(pk=pk)

        if not request.user.has_perm('mail_service.can_finish_mailing'):
            return HttpResponseForbidden("У вас нет прав для отключения рассылки.")
        else:
            finish_mailing.status = 'completed'
            finish_mailing.save()
        return redirect(reverse("mail_service:mailing_list"))
