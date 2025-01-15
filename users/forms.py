from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from mail_service.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'avatar', 'country')
