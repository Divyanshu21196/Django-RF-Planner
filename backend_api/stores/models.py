from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

class Store(models.Model):
    name = models.CharField(max_length=255, unique=True,help_text="Store name")
    address = models.TextField(help_text="Store address")
    town = models.CharField(max_length=100, help_text="Town or city")
    country = models.CharField(max_length=100, help_text="Country")
    county = models.CharField(max_length=100, blank=True, null=True, help_text="County or state")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    phone_number = models.CharField(
        max_length=15,
        validators=[phone_regex],
        help_text="Phone number",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='stores',help_text="User who created the store", on_delete=models.CASCADE, null=True)
    updated_by = models.ForeignKey(User, related_name='stores_updated', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-created_at']
        db_table = "stores"

    def __str__(self):
        return f"{self.name} - {self.town}, {self.country}"