from django.urls import path
from django.views.decorators.cache import cache_page

from mail_service.apps import MailServiceConfig
from mail_service.views import ClientListView, ClientDetailView, home_view, ClientUpdateView, ClientCreateView, \
    ClientDeleteView, MessageListView, MessageDetailView, MessageUpdateView, MessageCreateView, MessageDeleteView, \
    MailingListView, MailingDetailView, MailingUpdateView, MailingCreateView, MailingDeleteView

app_name = MailServiceConfig.name


urlpatterns = [
    path('', home_view, name='home'),
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing/list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
]