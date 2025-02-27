from django.contrib import admin
from .models import Loan, LoanRequest , LoanPlan , MonthlyRepayment

# Register your models here.
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'loan_customer', 'loan_provider', 'loan_amount', 'loan_status', 'created_at']
    list_filter = ['loan_status', 'created_at']
    search_fields = ['loan_customer__user__username', 'loan_provider__user__username']

@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider', 'loan', 'created_at',]
    list_filter = ['loan', 'provider']
    search_fields = ['provider__user__username']

@admin.register(LoanPlan)
class LoanPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'interest_rate', 'max_loan_amount', 'min_loan_amount', 'max_loan_duration', 'min_loan_duration']
    list_filter = ['name', 'interest_rate', 'max_loan_amount', 'min_loan_amount', 'max_loan_duration', 'min_loan_duration']
    search_fields = ['name']


@admin.register(MonthlyRepayment)
class MonthlyRepaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'loan', 'amount', 'date', 'paid']
    list_filter = ['loan', 'date', 'paid']
    search_fields = ['loan__loan_customer__user__username', 'loan__loan_provider__user__username']
