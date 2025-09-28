
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_super_user = models.BooleanField(default=False, help_text='Designates whether this user can manage all resources.')
    is_retailer = models.BooleanField(default=False, help_text='Designates whether this user is a retailer.')
    is_salesrep = models.BooleanField(default=False, help_text='Designates whether this user is a sales representative.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'custom_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"