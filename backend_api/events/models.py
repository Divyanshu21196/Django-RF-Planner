from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


User = get_user_model()


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('account_management', 'Account Management Event'),
        ('store_acquisition', 'Store Acquisition'),
    ]

    name = models.CharField(max_length=255,help_text="Name of the event")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES,help_text="Type of the event")
    start_date = models.DateField(help_text="Start date of the event")
    end_date = models.DateField(help_text="End date of the event")

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,help_text="Contact phone number for the event")

    #For Account Management events
    store =  models.ForeignKey('stores.Store', on_delete=models.CASCADE, null=True, blank=True, related_name='events',help_text="Associated store for Account Management events")

    #For Store Acquisition events
    store_location = models.TextField(null=True, blank=True,help_text="Location details for Store Acquisition events")

    store_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,help_text="Store contact phone number for Store Acquisition events")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events',help_text="User who created the event")
    created_at = models.DateTimeField(auto_now_add=True,help_text="Timestamp when the event was created")
    updated_at = models.DateTimeField(auto_now=True,help_text="Timestamp when the event was last updated")
    is_active = models.BooleanField(default=True,help_text="Indicates if the event is active")

    class Meta:
        db_table = 'events'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_event_type_display()})"

    def clean(self):
        #validate that start_date is before end_date
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date.")

        #Validate required fields based on event_type
        if self.event_type == 'account_management':
            if not self.store:
                raise ValidationError("Store is required for Account Management events.")
        elif self.event_type == 'store_acquisition':
            if not self.store_location:
                raise ValidationError("Store location is required for Store Acquisition events.")

            if not self.store_phone_number:
                raise ValidationError("Store phone number is required for Store Acquisition events.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean method to validate before saving
        super().save(*args, **kwargs)