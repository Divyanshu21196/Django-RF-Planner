from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'town', 'country', 'created_by', 'created_at')
    list_filter = ('country', 'town', 'created_at')
    search_fields = ('name', 'address', 'town', 'country')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Store Information', {
            'fields': ('name', 'address', 'town', 'country', 'county', 'phone_number')
        }),
        ('Meta Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )