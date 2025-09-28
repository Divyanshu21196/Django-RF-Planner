from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomerUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','first_name','last_name','is_super_user','is_retailer','is_salesrep','is_staff')
    list_filter = ('is_super_user','is_retailer','is_salesrep','is_staff','is_active')
    fieldsets = (
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':('first_name','last_name')}),
        ('User Type',{'fields':('is_super_user','is_retailer','is_salesrep')}),
        ('Permissions',{
            'fields':('is_active','is_staff','is_superuser','groups','user_permissions'),
        }),
        ('Important dates',{'fields':('last_login','date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_super_user', 'is_retailer', 'is_salesrep'),
        }),
    )

    search_fields = ('emeail',)
    ordering = ('email',)


admin.site.register(CustomUser,CustomerUserAdmin)