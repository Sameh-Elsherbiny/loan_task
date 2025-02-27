from django.db import models
from django.utils.translation import gettext_lazy as _

class UserTypes(models.TextChoices):
    USER = 'LP', _('LoanProvider'),
    Loan_Customer = 'LC', _('Loan'),
    The_Bank = 'BK', _('Bank'),
    

