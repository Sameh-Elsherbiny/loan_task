from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .choices import UserTypes
from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    user_type = models.CharField(
        max_length=2,
        choices=UserTypes.choices,
    )
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    first_name = None
    last_name = None

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class LoanProvider(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="loan_provider"
    )

    def __str__(self):
        return self.user.username


class LoanCustomer(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="loan_customer"
    )
    plan = models.ForeignKey(
        "loan.LoanPlan", on_delete=models.CASCADE, related_name="customer_plan", null=True, blank=True
    )

    def __str__(self):
        return self.user.username
    
class Bank(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="bank"
    )


class Account(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="account"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username
