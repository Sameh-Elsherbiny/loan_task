from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.apps import apps

def calculate_repayments(loan):

    """Calculate total and monthly repayment for a loan."""
    loan.interest_rate = loan.loan_customer.plan.interest_rate
    loan.total_repayment = loan.loan_amount + (
        loan.loan_amount * loan.interest_rate * loan.loan_duration / 100
    )
    loan.monthly_repayment = loan.total_repayment / loan.loan_duration

def approve_loan(loan):
    """Handles loan approval logic."""
    loan.loan_status = 'A'
    loan_provider = loan.loan_provider
    loan_customer = loan.loan_customer
    loan_provider.user.account.balance -= loan.loan_amount
    loan_provider.user.account.save()
    loan_customer.user.account.balance += loan.loan_amount
    loan_customer.user.account.save()
    loan.save()
    return loan

def create_monthly_repayments(loan):
    """Create monthly repayments for a loan."""
    monthly_repayment = loan.monthly_repayment
    for month in range(1, loan.loan_duration + 1):
        MonthlyRepayment = apps.get_model('loan', 'MonthlyRepayment')
        MonthlyRepayment.objects.create(
            loan=loan, amount=monthly_repayment, date=(datetime.now().replace(day=1) + relativedelta(months=month))
        )