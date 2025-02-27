from django.db import models
from .choices import LoanStatus
from .validators import validate_loan_constraints , validate_loan_request
from .utils import calculate_repayments

# Create your models here.


class LoanPlan(models.Model):
    name = models.CharField(max_length=50)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_loan_duration = models.IntegerField()
    min_loan_duration = models.IntegerField()
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    allowness = models.IntegerField(default=True)
    def __str__(self):
        return self.name


class Loan(models.Model):
    loan_status = models.CharField(
        max_length=10, choices=LoanStatus.choices, default=LoanStatus.REQUESTED
    )
    loan_customer = models.ForeignKey(
        "users.LoanCustomer", on_delete=models.CASCADE, related_name="loans_customer"
    )
    loan_provider = models.ForeignKey(
        "users.LoanProvider", on_delete=models.CASCADE, related_name="loans_provider", null=True , blank=True 
    )
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_duration = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_repayment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.loan_customer.user.username} - {self.loan_amount}"

    def clean(self):
        """Validate the loan using an external validation function."""
        validate_loan_constraints(self)
        super().clean()

    def save(self, *args, **kwargs):
        """Calculate repayments before saving."""
        self.full_clean()  # Ensures validation runs before saving
        calculate_repayments(self)
        super().save(*args, **kwargs)

class LoanRequest(models.Model):
    provider = models.ForeignKey(
        "users.LoanProvider", on_delete=models.CASCADE, related_name="loan_requests"
    )
    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name="requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider.user.username} - {self.loan}"
    
    def clean(self):
        """Validate the loan request using an external validation function."""
        validate_loan_request(self)
        super().clean()

    def save(self, *args, **kwargs):
        """Validate the loan request before saving."""
        self.full_clean()
        super().save(*args, **kwargs)
    
class MonthlyRepayment(models.Model):
    paid = models.BooleanField(default=False)
    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name="repayments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    over_due = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.loan} - {self.amount} - {self.date}"
    

