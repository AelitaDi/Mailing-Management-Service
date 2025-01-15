import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User

from config.settings import EMAIL_HOST_USER, DEBUG


class UserCreateView(CreateView):
    """
    Контроллер для регистрации пользователя.
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{user.token}/'
        send_mail(subject='Подтверждение регистрации',
                  message=f'Спасибо за регистрацию на нашем сайте!\nДля завершения регистрации пройдите по ссылке:\n{url}',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email, ])
        if DEBUG:
            print(url)
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования данных пользователя.
    """
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('mail_service:home')

    @staticmethod
    def block_user(request, pk):
        block_user = User.objects.get(pk=pk)

        if not request.user.has_perm('users.can_block_user'):
            return HttpResponseForbidden("У вас нет прав для блокировки пользователя.")
        else:
            block_user.is_blocked = True
            block_user.save()
        return redirect(reverse("users:user_list"))


def profile_view(request):
    """
    Контроллер для просмотра данных пользователя.
    """
    user = request.user
    context = {'user': user, }
    return render(request, context=context, template_name='users/profile.html')


def email_verification(request, token):
    """
    Верификация пользователя.
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс для отображения списка пользователей.
    """
    model = User
    permission_required = "users.view_user"
    context_object_name = "users"
