from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário totalmente customizado.
    """
    email = models.EmailField(
        verbose_name="Endereço de email",
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(
        verbose_name="Nome Completo",
        max_length=255
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        O usuário tem uma permissão específica?
        A maneira mais simples e correta é delegar para is_staff.
        """
        return self.is_staff

    def has_module_perms(self, app_label: str):
        """
        O usuário tem permissões para ver o app `app_label`?
        Simplesmente checar se é staff é suficiente para acesso ao admin.
        """
        return self.is_staff
