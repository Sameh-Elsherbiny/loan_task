from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError as DRFValidationError

def validate_loan_constraints(loan):
    """Validate loan amount and duration based on the customer's loan plan."""
    errors = []

    if not loan.loan_customer or not loan.loan_customer.plan:
        errors.append("Loan customer or plan details are missing.")

    if not errors:
        plan = loan.loan_customer.plan  # Get the plan reference

        if loan.loan_amount > plan.max_loan_amount:
            errors.append("Loan amount exceeds the maximum limit.")
        if loan.loan_amount < plan.min_loan_amount:
            errors.append("Loan amount is below the minimum limit.")
        if loan.loan_duration > plan.max_loan_duration:
            errors.append("Loan duration exceeds the maximum limit.")
        if loan.loan_duration < plan.min_loan_duration:
            errors.append("Loan duration is below the minimum limit.")

    if errors:
        raise DRFValidationError(errors, code=400)


from django.db.models import Sum
from django.core.exceptions import ValidationError

def validate_loan_request(loan_request):
    """Validate that a loan request is not made by a loan provider with insufficient funds."""

    # Get total pending/requested loan amounts for this provider
    loans = loan_request.provider.loans_provider.filter(
        loan_status__in=["PENDING", "REQUESTED"]
    ).aggregate(total_loan_amount=Sum("loan_amount"))  # Aggregating loan amount

    # Get total loan requests for this provider
    requests = loan_request.provider.loan_requests.aggregate(
        total_request_amount=Sum("loan__loan_amount")
    )

    # Ensure default value is 0 if aggregation returns None
    total_loans = loans.get("total_loan_amount") or 0
    total_requests = requests.get("total_request_amount") or 0
    total_funds_needed = total_loans + total_requests

    # Get provider's available balance
    provider_balance = loan_request.provider.user.account.balance

    # Validation check
    if total_funds_needed > provider_balance:
        raise ValidationError("Insufficient funds to provide loans.")


# def validate_loan_id(loan_id):
#     """Ensure the loan exists before proceeding."""
#     if not Loan.objects.filter(id=loan_id).exists():
#         raise ValidationError("Invalid loan ID")
#     return loan_id