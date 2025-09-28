from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'start_date', 'end_date', 'created_by', 'created_at')
    list_filter = ('event_type', 'start_date', 'created_at')
    search_fields = ('name', 'store_location')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Event Information', {
            'fields': ('name', 'event_type', 'start_date', 'end_date', 'phone_number')
        }),
        ('Account Management Event', {
            'fields': ('store',),
            'classes': ('collapse',),
        }),
        ('Store Acquisition Event', {
            'fields': ('store_location', 'store_phone_number'),
            'classes': ('collapse',),
        }),
        ('Meta Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.event_type == 'account_management':
            # Show only relevant fieldsets for account management
            return [fieldsets[0], fieldsets[1], fieldsets[3]]
        elif obj and obj.event_type == 'store_acquisition':
            # Show only relevant fieldsets for store acquisition
            return [fieldsets[0], fieldsets[2], fieldsets[3]]
        return fieldsets