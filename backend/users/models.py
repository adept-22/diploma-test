from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#Переделанная модель Пользователи
class Users(AbstractUser):
    ACCESS = [
        ('Administrator', 'Administrator'),
        ('User', 'User')
    ]
    DEFAULT_ACCESS = 'User'

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name = 'Уникальный юзернейм'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name = 'Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name = 'Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    access = models.CharField(
        max_length=15,
        choices=ACCESS,
        default=DEFAULT_ACCESS,
        verbose_name='Роль доступа',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

