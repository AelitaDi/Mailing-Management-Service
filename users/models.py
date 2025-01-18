from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=150, verbose_name="Страна", help_text="Введите страну", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        help_text="Загрузите ваш аватар",
        blank=True,
        null=True,
    )

    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True, )

    is_blocked = models.BooleanField(default=False, verbose_name="заблокирован")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email']
        permissions = [
            ("can_block_user", "Can block user"),
        ]

    def __str__(self):
        return self.email
