from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import RegisterForm
from django.contrib import admin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model=CustomUser
    add_form=RegisterForm
    ordering = ('email',)
    list_display = ('email','is_active','last_login','is_staff')
    list_filter = ('is_active','is_staff','last_login')
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
    )


admin.site.register(CustomUser,CustomUserAdmin)