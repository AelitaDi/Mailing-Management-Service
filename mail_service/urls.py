from django.urls import path
from django.views.decorators.cache import cache_page

from mail_service.apps import MailServiceConfig
from mail_service.views import ClientListView
# ProductDetailView, ProductCreateView, ContactsListView, ProductUpdateView, \
#     ProductDeleteView, CategoryDetailView

app_name = MailServiceConfig.name


urlpatterns = [
    path('clients/list/', ClientListView.as_view(), name='client_list'),
    # path('contacts/list/', ContactsListView.as_view(), name='contacts_list'),
    # path('', ProductListView.as_view(), name='product_list'),
    # path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    # path('product/create/', ProductCreateView.as_view(), name='product_create'),
    # path('product/update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    # path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
    # path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
]