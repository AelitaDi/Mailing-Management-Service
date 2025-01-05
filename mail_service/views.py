from django.shortcuts import render
from django.views.generic import ListView
from mail_service.models import Client


class ClientListView(ListView):
    model = Client
    paginate_by = 5
