from django.contrib import admin
from .models import CustomUser , LoanProvider , LoanCustomer , Account , Bank

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username',)
    ordering = ('username',)

@admin.register(LoanProvider)
class LoanProviderAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user__username',)
    ordering = ('user',)

@admin.register(LoanCustomer)
class LoanCustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan')
    search_fields = ('user__username', 'plan__name')
    ordering = ('user', 'plan')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)
    ordering = ('user',)

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user__username',)
    ordering = ('user',)