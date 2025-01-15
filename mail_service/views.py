from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config.settings import CACHE_ENABLED
from mail_service.forms import ClientForm, MessageForm, MailingForm
from mail_service.models import Client, Mailing, Message


def home_view(request):
    mailing_count = Mailing.objects.count()
    started_mailing_count = Mailing.objects.filter(status='started').count()
    clients = Client.objects.count()
    context = {
        'mailing_count': mailing_count,
        'started_mailing_count': started_mailing_count,
        'clients': clients,
    }
    return render(request, 'mail_service/home.html', context)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    # paginate_by = 5

    def get_queryset(self):
        if not CACHE_ENABLED:
            return super().get_queryset().filter(owner=self.request.user)
        key = "client_list"
        clients = cache.get(key)
        if clients is not None:
            return clients
        clients = super().get_queryset().filter(owner=self.request.user)
        cache.set(key, clients, 60 * 1)
        return clients


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail_service:home')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ClientForm
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
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
    model = Message
    # paginate_by = 5

    def get_queryset(self):
        if not CACHE_ENABLED:
            return super().get_queryset().filter(owner=self.request.user)
        key = "message_list"
        messages = cache.get(key)
        if messages is not None:
            return messages
        messages = super().get_queryset().filter(owner=self.request.user)
        cache.set(key, messages, 60 * 1)
        return messages


class MessageDeleteView(LoginRequiredMixin, DeleteView):
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
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
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
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        raise PermissionDenied
#
#


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    # paginate_by = 5

    def get_queryset(self):
        if not CACHE_ENABLED:
            return super().get_queryset().filter(owner=self.request.user)
        key = "mailing_list"
        mailings = cache.get(key)
        if mailings is not None:
            return mailings
        mailings = super().get_queryset().filter(owner=self.request.user)
        cache.set(key, mailings, 60 * 1)
        return mailings


class MailingDeleteView(LoginRequiredMixin, DeleteView):
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
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
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
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mail_service:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        raise PermissionDenied
