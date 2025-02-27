from django.db import models
from django.utils.translation import gettext_lazy as _

class LoanStatus(models.TextChoices):
    REQUESTED = 'RQ', _('Requested'),
    PENDING = 'P', _('Pending'),
    APPROVED = 'A', _('Approved'),
    REJECTED = 'R', _('Rejected'),
    PAID = 'PD', _('Paid'),
    