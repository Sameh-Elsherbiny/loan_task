from .models import Loan
from django.db.models import Q

class LoanService:
    @staticmethod
    def get_loans_for_user(user):
        """Return filtered loans based on user type."""
        if user.user_type == 'LP':
            return Loan.objects.filter(loan_provider__user=user)
        elif user.user_type == 'LC':
            return Loan.objects.filter(loan_customer__user=user)
        elif user.user_type == 'BK':
            return Loan.objects.all()
        return Loan.objects.none()
    
    